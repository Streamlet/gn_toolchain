import os, sys, locale, subprocess


def ExecuteCmd(cmd):
    encoding = locale.getpreferredencoding(False)
    (stdoutdata, stderrdata) = subprocess.Popen(cmd,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT,
                                                shell=True).communicate()
    if stderrdata is not None:
        print(stderrdata.decode(encoding))
        return False
    output = stdoutdata.decode(encoding)
    return output.strip()


def DetectVSByVSWhere():
    program_files_x86 = os.environ['ProgramFiles(x86)']
    vswhere_path = '%s\\Microsoft Visual Studio\\Installer\\vswhere.exe' % program_files_x86
    if not os.path.exists(vswhere_path):
        return None
    cmd = '"%s" -legacy -latest -property installationPath' % vswhere_path
    return ExecuteCmd(cmd)


def SetupEnvironment(host_cpu, target_cpu):
    vs_path = DetectVSByVSWhere()
    if vs_path is None:
        return False
    BATCH_FILES = {
        # host
        'x64': {
            # target
            'x64': 'vcvars64.bat',
            'x86': 'vcvarsamd64_x86.bat',
        },
        'x86': {
            'x64': 'vcvarsx86_amd64.bat',
            'x86': 'vcvars32.bat',
        },
    }
    batch_file = vs_path + '\\VC\\Auxiliary\\Build\\' + BATCH_FILES[host_cpu][target_cpu]
    lines = ExecuteCmd('"' + batch_file + '" && Set')
    ENV_VAR_TO_SAVE = ('INCLUDE', 'LIB', 'LIBPATH', 'PATH', 'PATHEXT', 'SYSTEMROOT', 'TEMP', 'TMP')
    env_block = ''
    for line in lines.split('\n'):
        kv = line.split('=', 2)
        if kv[0].upper() in ENV_VAR_TO_SAVE:
            env_block += line.strip() + '\0'
    env_block += '\0'
    with open('environment.%s.%s' % (host_cpu, target_cpu), 'w') as f:
        f.write(env_block)


def main():
    SetupEnvironment(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
