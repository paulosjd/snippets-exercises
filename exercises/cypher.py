import unittest


class Solution:

    def CeasarCypher(self, input, key):
        def shift(letter):
            start, end = (64, 90) if letter.isupper() else (96, 122)
            dec = ord(letter) + key
            if dec > end:
                dec = start + dec - end
            return dec
        letters = []
        for i in input:
            if i.isalpha():
                letters.append(chr(shift(i)))
            else:
                letters.append(i)
        return ''.join(letters)


class SolutionTests(unittest.TestCase):
    def test1(self):
        solution = Solution()
        self.assertEqual(solution.CeasarCypher("Zwddg ogjdv!", 8), "Hello world!")


if __name__ == '__main__':
    unittest.main()