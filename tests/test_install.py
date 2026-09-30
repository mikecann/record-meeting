import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def test_installer_can_be_rerun_without_touching_other_commands(self):
        with tempfile.TemporaryDirectory(prefix="record meeting install ") as directory:
            target = Path(directory) / "bin"
            target.mkdir()
            other_command = target / "another-tool"
            other_command.write_text("keep me")

            for _ in range(2):
                subprocess.run(
                    ["bash", str(ROOT / "install.sh"), str(target)],
                    cwd=directory,
                    check=True,
                    capture_output=True,
                    text=True,
                )

            self.assertTrue((target / "record-meeting").is_symlink())
            self.assertEqual((target / "record-meeting").resolve(), ROOT / "record-meeting")
            self.assertEqual(other_command.read_text(), "keep me")

    def test_symlinked_launcher_finds_setup_in_its_clone(self):
        with tempfile.TemporaryDirectory(prefix="record meeting launcher ") as directory:
            root = Path(directory)
            clone = root / "clone with spaces"
            clone.mkdir()
            shutil.copy2(ROOT / "record-meeting", clone / "record-meeting")
            (clone / "setup_mac.sh").write_text('printf "setup from clone\\n"\n')
            bin_directory = root / "bin"
            bin_directory.mkdir()
            launcher = bin_directory / "record-meeting"
            # Match the absolute symlink made by install.sh.
            launcher.symlink_to(clone / "record-meeting")

            result = subprocess.run(
                [str(launcher), "setup"],
                cwd=root,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "setup from clone\n")


if __name__ == "__main__":
    unittest.main()
