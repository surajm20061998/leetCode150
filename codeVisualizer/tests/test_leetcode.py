import unittest

from server.app.leetcode import extract_slug, parse_sample_args


class LeetCodeParsingTests(unittest.TestCase):
    def test_extracts_slug(self):
        self.assertEqual(
            extract_slug("https://leetcode.com/problems/diameter-of-binary-tree/description/?envType=study-plan"),
            "diameter-of-binary-tree",
        )

    def test_rejects_non_leetcode_domain(self):
        with self.assertRaisesRegex(ValueError, "leetcode.com"):
            extract_slug("https://example.com/problems/two-sum/")

    def test_groups_sample_arguments_by_parameter_count(self):
        source = "[2,7,11,15]\n9\n[3,2,4]\n6"
        self.assertEqual(
            parse_sample_args(source, 2),
            [[[2, 7, 11, 15], 9], [[3, 2, 4], 6]],
        )


if __name__ == "__main__":
    unittest.main()
