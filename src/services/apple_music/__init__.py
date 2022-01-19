from .api import AppleMusicApi

import applemusicpy


def patch_lib() -> None:
    def generate_token_stub(self, x) -> None:
        self.token_str = self._secret_key

    def token_is_valid_stub(self) -> bool:
        return True

    applemusicpy.AppleMusic.generate_token = generate_token_stub
    applemusicpy.AppleMusic.token_is_valid = token_is_valid_stub


patch_lib()
