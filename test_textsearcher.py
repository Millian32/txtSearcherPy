import unittest
import textsearcher


class MyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.shortsearcher = textsearcher.TextSearcher('files/short_excerpt.txt')
        self.longsearcher = textsearcher.TextSearcher('files/long_excerpt.txt')

    # Simplest possible case, no context and the word occurs exactly once.
    def test_OneHitNoContext(self):
        expected = [
            'sketch',
        ]
        results = self.shortsearcher.search('sketch', 0)
        self.assertEqual(expected, results)

    # Next simplest case, no context and multiple hits
    def test_MultipleHitsNoContext(self):
        expected = [
            "naturalists",
            "naturalists,"
        ]
        results = self.shortsearcher.search("naturalists", 0)
        self.assertEqual(expected, results)

    # This is the example from the document
    def test_BasicSearch(self):
        expected = [
            "great majority of naturalists believed that species",
            "authors.  Some few naturalists, on the other"
        ]
        searcher = textsearcher.TextSearcher('files/short_excerpt.txt')
        results = self.shortsearcher.search("naturalists", 3)
        self.assertEqual(expected, results)

    # Same as basic search but a little more context
    def test_BasicMoreContext(self):
        expected = [
            "Until recently the great majority of naturalists believed that species were immutable productions",
            "maintained by many authors.  Some few naturalists, on the other hand, have believed"
        ]
        searcher = textsearcher.TextSearcher('files/short_excerpt.txt')
        results = self.shortsearcher.search("naturalists", 6)
        self.assertEqual(expected, results)

    # Tests query word with apostrophe
    def test_ApostropheQuery(self):
        expected = [
            "not indeed to the animal's or plant's own good,",
            "habitually speak of an animal's organisation as\nsomething plastic,"
        ]
        searcher = textsearcher.TextSearcher('files/long_excerpt.txt')
        results = self.longsearcher.search("animal's", 4)
        self.assertEqual(expected, results)

    # Tests numeric query word
    def test_NumericQuery(self):
        expected = [
            "enlarged in 1844 into a",
            "sketch of 1844--honoured me"
        ]
        searcher = textsearcher.TextSearcher('files/long_excerpt.txt')
        results = self.longsearcher.search("1844", 2)
        self.assertEqual(expected, results)

    # Tests mixed alphanumeric query word
    def test_testMixedQuery(self):
        expected = [
            "date first edition [xxxxx10x.xxx] please check file"
        ]
        searcher = textsearcher.TextSearcher('files/long_excerpt.txt')
        results = self.longsearcher.search("xxxxx10x", 3)
        self.assertEqual(expected, results)

    # Should get same results regardless of case
    def test_CaseInsensitiveSearch(self):
        expected = [
            "on the Origin of Species.  Until recently the great",
            "of naturalists believed that species were immutable productions, and",
            "hand, have believed that species undergo modification, and that"
        ]

        results = self.shortsearcher.search("species", 4)
        self.assertEqual(expected, results)

        results = self.shortsearcher.search("SPECIES", 4)
        self.assertEqual(expected, results)

        results = self.shortsearcher.search("SpEcIeS", 4)
        self.assertEqual(expected, results)

    # Hit that overlaps file start should still work. */
    def test_testNearBeginning(self):
        expected = [
            "I will here give a brief sketch"
        ]
        results = self.shortsearcher.search("here", 4)
        self.assertEqual(expected, results)

    # Hit that overlaps file end should still work. */
    def test_NearEnd(self):
        expected = [
            "and that the existing forms of life",
            "generation of pre existing forms."
        ]
        results = self.shortsearcher.search("existing", 3)
        self.assertEqual(expected, results)

    # Overlapping hits should just come back as separate hits. */
    def test_OverlappingHits(self):
        expected = [
            "of naturalists believed that species were immutable",
            "hand, have believed that species undergo modification,",
            "undergo modification, and that the existing forms"
        ]
        results = self.shortsearcher.search("that", 3)
        self.assertEqual(expected, results)

    # If no hits, get back an empty array. */
    def test_NoHits(self):
        results = self.shortsearcher.search("slejrlskejrlkajlsklejrlksjekl", 3)
        self.assertEqual(0, len(results))

    def test_TextSearcherReturnsNone(self):
        # pass bogus file
        results = self.shortsearcher.__init__('./aNonExistentFile.txt')
        self.assertIsNone(results)

    def test_BasicSearch2(self):
        expected = [
                "believed that species undergo modification, and that"
            ]
        searcher = textsearcher.TextSearcher('files/short_excerpt.txt')
        results = self.shortsearcher.search("undergo", 3)
        self.assertEqual(expected, results)


if __name__ == '__main__':
    unittest.main()
