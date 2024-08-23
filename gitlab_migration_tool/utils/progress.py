from git import RemoteProgress
from tqdm import tqdm# type: ignore

class ProgressBar(RemoteProgress):
    def __init__(self, description="Progress"):
        super().__init__()
        self.pbar = tqdm(
            total=100,
            unit="%",
            desc=description,
            ncols=100,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
            leave=True
        )

    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count:
            self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.set_postfix_str(message)
        
        # Adjust color of the bar as it progresses
        progress = cur_count / max_count if max_count else 0
        color = self._get_color(progress)
        
        self.pbar.bar_format = f"{{l_bar}}{color}{{bar}}\033[0m| {{n_fmt}}/{{total_fmt}} [{{elapsed}}<{{remaining}}, {{rate_fmt}}{{postfix}}]"
        self.pbar.refresh()

    def _get_color(self, progress):
        """Return the color code based on progress."""
        if progress < 0.5:
            return '\033[91m'  # Red
        elif progress < 0.75:
            return '\033[93m'  # Yellow
        else:
            return '\033[92m'  # Green

    def __del__(self):
        self.pbar.close()

class CloneProgress(ProgressBar):
    def __init__(self):
        super().__init__(description="Cloning Progress")

class PushProgress(ProgressBar):
    def __init__(self):
        super().__init__(description="Pushing Progress")