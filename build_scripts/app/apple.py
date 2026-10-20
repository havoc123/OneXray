import os

from app.builder import Builder
from app.command_line import run_command

DEFAULT_LANE = "deploy"


class AppleBuilder(Builder):
    def before_build(self):
        super().before_build()
        run_command(
            ["xcrun", "agvtool", "new-version", "-all", str(self.build_number)],
            cwd=self.project_dir,
        )

    def build_app(self):
        # ONEXRAY_IOS_LANE selects an alternative fastlane lane (for example
        # `unsigned` or `adhoc`) so self-signed builds can skip TestFlight.
        lane = os.environ.get("ONEXRAY_IOS_LANE") or DEFAULT_LANE
        run_command(["fastlane", lane, "--verbose"], cwd=self.project_dir)
