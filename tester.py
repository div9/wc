import shlex
import subprocess
import unittest


def run_piped_commands(commands, shell=False):
    """
    Run a series of piped commands and return the output
    >>> run_piped_commands(["cat ./test.txt", "wc"])
    """
    assert commands, "No commands provided"

    # if there's only one command, just run it
    if len(commands) == 1:
        return run_command(commands[0], shell=shell)

    # print(f"Running piped command: {' | '.join(commands)}")
    if shell:
        split_commands = commands
    else:
        split_commands = [shlex.split(command) for command in commands]
    processes = [
        subprocess.Popen(
            split_commands[0],
            stdout=subprocess.PIPE,
            shell=shell,
        )
    ]

    # make each process pipe its output to the next process
    for i in range(1, len(split_commands)):
        new_process = subprocess.Popen(
            split_commands[i],
            stdin=processes[i - 1].stdout,
            stdout=subprocess.PIPE,
            shell=shell,
        )
        processes.append(new_process)

    # wait for each process to finish
    for i in range(len(processes) - 1):
        pipe = processes[i]
        pipe.wait()
        if pipe.stdout:
            pipe.stdout.close()

    # return the output of the last process
    return processes[-1].communicate()[0].decode("utf-8").strip()


def run_command(command, shell=False):
    """
    Run a command and return the output
    """
    # print(f"Running command: {command}")
    if shell:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    else:
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    return process.communicate()[0].decode("utf-8").strip()


class TestCCWC(unittest.TestCase):
    def testLines(self):
        wc_output = run_command("wc -l ./test.txt")
        ccwc_output = run_command("./ccwc -l ./test.txt")
        self.assertEqual(wc_output, ccwc_output)

    def testBytes(self):
        wc_output = run_command("wc -c ./test.txt")
        ccwc_output = run_command("./ccwc -c ./test.txt")
        self.assertEqual(wc_output, ccwc_output)

    def testWords(self):
        wc_output = run_command("wc -w ./test.txt")
        ccwc_output = run_command("./ccwc -w ./test.txt")
        self.assertEqual(wc_output, ccwc_output)

    def testChars(self):
        wc_output = run_command("wc -m ./test.txt")
        ccwc_output = run_command("./ccwc -m ./test.txt")
        self.assertEqual(wc_output, ccwc_output)

    def testNoOptions(self):
        wc_output = run_command("wc ./test.txt")
        ccwc_output = run_command("./ccwc ./test.txt")
        self.assertEqual(wc_output, ccwc_output)

    def testTwoOptions(self):
        options = ["-wl", "-cl", "-wc"]
        for option in options:
            wc_output = run_command(f"wc {option} ./test.txt")
            ccwc_output = run_command(f"./ccwc {option} ./test.txt")
            self.assertEqual(wc_output, ccwc_output)

    def testMultipleFiles(self):
        wc_output = run_command("wc ./test.txt ./ccwc")
        ccwc_output = run_command("./ccwc ./test.txt ./ccwc")
        self.assertEqual(wc_output, ccwc_output)

    def testFileGlobs(self):
        wc_output = run_command("wc *", shell=True)
        ccwc_output = run_command("./ccwc *", shell=True)
        self.assertEqual(wc_output, ccwc_output)

    def testStandardInput(self):
        wc_commands = ["cat ./test.txt", "wc"]
        ccwc_commands = ["cat ./test.txt", "./ccwc"]
        wc_output = run_piped_commands(wc_commands)
        ccwc_output = run_piped_commands(ccwc_commands)
        self.assertEqual(wc_output, ccwc_output)


if __name__ == "__main__":
    unittest.main()
