# Copyright (c) 2026 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

class MenuBtn:
    """
    Represents a menu button with ID and callback data.

    Encapsulates button configuration including unique identifier and
    callback data for handling button interactions in inline keyboards.
    """

    btn_cbk: str
    btn_id: str

    def __init__(self,
                 btn_id: str,
                 btn_cbk: str = "") -> None:
        """
        Initialize a menu button.

        Args:
            btn_id: The unique identifier for the button.
            btn_cbk: The callback data associated with the button. Defaults to empty string.
        """
        self.btn_cbk = btn_cbk
        self.btn_id = btn_id

    def Id(self) -> str:
        """
        Get the button's unique identifier.

        Returns:
            The button ID.
        """
        return self.btn_id

    def Callback(self) -> str:
        """
        Get the button's callback data.

        Returns:
            The callback data.
        """
        return self.btn_cbk
