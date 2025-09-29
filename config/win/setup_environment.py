import os
import sys
import locale
import subprocess
import re
import winreg


VC_60_VERSION = 60
VS_2002_VERSION = 70
VS_2003_VERSION = 71
VS_2005_VERSION = 80
VS_2008_VERSION = 90
VS_2010_VERSION = 100
VS_2012_VERSION = 110
VS_2013_VERSION = 120
VS_2015_VERSION = 140
VS_2017_VERSION = 150
VS_2019_VERSION = 160
VS_2022_VERSION = 170


def ExecuteCmd(cmd):
    encoding = locale.getpreferredencoding(False)
    (stdoutdata, stderrdata) = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).communicate()
    if stderrdata is not None:
        print(stderrdata.decode(encoding))
        return False
    output = stdoutdata.decode(encoding)
    return output.strip()


def DetectSetEnvBatchFileByVSWhere(host_cpu, target_cpu):
    program_files_x86 = os.environ['ProgramFiles(x86)']
    vswhere_path = os.path.join(
        program_files_x86, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe')
    if not os.path.exists(vswhere_path):
        return None, None
    cmd = '"%s" -latest -property installationPath' % vswhere_path
    vs_path = ExecuteCmd(cmd)
    if vs_path is None or vs_path == '':
        return None, None
    cmd = '"%s" -latest -property installationVersion' % vswhere_path
    vs_version_string = ExecuteCmd(cmd)
    if vs_version_string is None or vs_version_string == '':
        return None, None
    vs_version_part = list(map(lambda x: int(x), vs_version_string.split('.')))
    if len(vs_version_part) < 2:
        return None, None
    vs_version = vs_version_part[0] * 10 + (min(vs_version_part[1], 9))
    batch_file = os.path.join(
        vs_path, 'VC', 'Auxiliary', 'Build', 'vcvarsall.bat')
    if not os.path.exists(batch_file):
        return None, None
    if host_cpu == target_cpu:
        arch = target_cpu
    else:
        arch = host_cpu + '_' + target_cpu
    return vs_version, [batch_file, arch]


def DetectSetEnvBatchFileByEnvVar(expected_vs_version, host_cpu, target_cpu):
    regex = re.compile(r'VS(\d+)COMNTOOLS')
    vs_versions = []
    for vs in os.environ:
        m = regex.match(vs.upper())
        if m:
            vs_versions.append((int(m.group(1)), os.environ[vs]))
    vs_versions = sorted(vs_versions, key=lambda item: item[0], reverse=True)
    if expected_vs_version > 0:
        vs_versions = [ item for item in vs_versions if item[0] == expected_vs_version ]
    for version, path in vs_versions:
        if version > VS_2003_VERSION:
            batch_file = os.path.join(path, '..', '..', 'VC', 'vcvarsall.bat')
            if os.path.exists(batch_file):
                if host_cpu == target_cpu:
                    arch = target_cpu
                else:
                    arch = host_cpu + '_' + target_cpu
                return version, [batch_file, arch]
        else:
            batch_file = os.path.join(path, 'vsvars32.bat')
            if os.path.exists(batch_file):
                return version, [batch_file]
    return None, None


def DetectSetEnvBatchFileByFindVC6(host_cpu, target_cpu):
    program_files_x86 = os.environ['ProgramFiles(x86)']
    batch_file = os.path.join(
        program_files_x86, 'Microsoft Visual Studio', 'VC98', 'Bin', 'vcvars32.bat')
    if not os.path.exists(batch_file):
        return None, None
    return VC_60_VERSION, [batch_file]


def FindWinSDK7(host_cpu, target_cpu):
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Microsoft SDKs\Windows', 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as key:
        sdk_dir, type = winreg.QueryValueEx(key, "CurrentInstallFolder")
    include_path = os.path.join(sdk_dir, 'Include')
    lib_path = os.path.join(sdk_dir, 'Lib')
    if target_cpu == 'x64':
        lib_path = os.path.join(lib_path, 'x64')
    if not os.path.exists(include_path) or not os.path.exists(lib_path):
        return None, None, None
    return [os.path.join(sdk_dir, 'bin', 'setenv.cmd'), '/' + target_cpu], include_path, lib_path


def SetupEnvironment(expected_vs_version, host_cpu, target_cpu, is_winxp):
    version, cmd = DetectSetEnvBatchFileByVSWhere(host_cpu, target_cpu)
    if cmd is None or (expected_vs_version > 0 and version != expected_vs_version):
        version, cmd = DetectSetEnvBatchFileByEnvVar(expected_vs_version, host_cpu, target_cpu)
    if cmd is None or (expected_vs_version > 0 and version != expected_vs_version):
        version, cmd = DetectSetEnvBatchFileByFindVC6(host_cpu, target_cpu)
    if cmd is None and not is_winxp:
        assert False, 'Cannot find Windows SDK set-env batch file'
    shell_cmd = '"%s" %s && Set' % (cmd[0], ' '.join(cmd[1:]))
    env_lines = ExecuteCmd(shell_cmd)
    env_ok = 'INCLUDE' in env_lines
    if not env_ok or (expected_vs_version > 0 and version != expected_vs_version) or is_winxp:
        cmd, include_path, lib_path = FindWinSDK7(host_cpu, target_cpu)
        if include_path is None or lib_path is None:
            assert False, 'Cannot find Windows SDK.'
        if not env_ok:
            shell_cmd = '"%s" %s && Set' % (cmd[0], ' '.join(cmd[1:]))
            env_lines = ExecuteCmd(shell_cmd)
    ENV_VAR_TO_SAVE = (
        'INCLUDE',
        'LIB',
        'LIBPATH',
        'PATH',
        'PATHEXT',
        'SYSTEMROOT',
        'TEMP',
        'TMP',
    )
    env = {}
    for line in env_lines.split('\n'):
        kv = line.split('=', 2)
        if kv[0].upper() in ENV_VAR_TO_SAVE:
            env[kv[0].upper()] = kv[1].strip()
    if is_winxp:
        if version > VS_2017_VERSION:
            vc141_version_file = os.path.join(os.path.dirname(
                cmd[0]), 'Microsoft.VCToolsVersion.v141.default.txt')
            vc_version_file = os.path.join(os.path.dirname(
                cmd[0]), 'Microsoft.VCToolsVersion.default.txt')
            if not os.path.exists(vc141_version_file):
                assert False, 'v141_xp toolset not installed'
            with open(vc141_version_file, 'r') as f:
                vc141_version = f.read().strip()
            with open(vc_version_file, 'r') as f:
                vc_version = f.read().strip()
            env['INCLUDE'] = env['INCLUDE'].replace(vc_version, vc141_version)
            env['LIB'] = env['LIB'].replace(vc_version, vc141_version)
            env['LIBPATH'] = env['LIBPATH'].replace(vc_version, vc141_version)
            env['PATH'] = env['PATH'].replace(vc_version, vc141_version)

        env['INCLUDE'] = include_path + ';' + env['INCLUDE']
        env['LIB'] = lib_path + ';' + env['LIB']
        env['LIBPATH'] = lib_path + ';' + env['LIBPATH']

    env_file_content = ''
    for k in env:
        env_file_content += k + '=' + env[k] + '\0'
    env_file_content += '\0'
    with open('environment.%s.%s' % (host_cpu, target_cpu), 'w') as f:
        f.write(env_file_content)
    return version, env


def FindExecutableInPath(env_path, exe_name):
    paths = env_path.split(';')
    for path in paths:
        if os.path.exists(os.path.join(path, exe_name)):
            return path
    return None


def FindCompiles(env_path):
    cl_path = FindExecutableInPath(env_path, 'cl.exe')
    return {'MSVC': cl_path}


def main():
    (expected_vs_version, host_cpu, target_cpu, is_winxp) = sys.argv[1:]
    version, env = SetupEnvironment(int(expected_vs_version), host_cpu, target_cpu, is_winxp == 'true')
    print('VERSION = %s' % (version if version is not None else ''))
    cc_path = FindCompiles(env['PATH'])
    for cc in cc_path:
        print('%s = %s' % (cc, 'true' if cc_path[cc] is not None else 'false'))


if __name__ == '__main__':
    main()
