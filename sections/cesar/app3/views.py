from django.http import HttpResponse

class Solution:
    def reverse(self, x: int) -> int:
        is_negative = x < 0
        x = abs(x)
        
        reversed_num = 0
        while x > 0:
            reversed_num = reversed_num * 10 + x % 10
            x //= 10
        
        if is_negative:
            reversed_num = -reversed_num
        
        if reversed_num < -2**31 or reversed_num > 2**31 - 1:
            return 0
        
        return reversed_num

def leetcode_app(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LeetCode - Reverse Integer</title>
    </head>
    <body>
        <h1>LeetCode: Reverse Integer</h1>
        <p>This app demonstrates the solution to the "Reverse Integer" problem.</p>
        <p>Example: reverse(123) = 321</p>
        <p>Example: reverse(-123) = -321</p>
    </body>
    </html>
    """
    return HttpResponse(html)