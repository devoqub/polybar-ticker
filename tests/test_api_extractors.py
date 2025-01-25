import json
import unittest

from src.api_extractors import (
    BaseAPIExtractor,
    GeminiAPIExtractor,
    get_extractor_class
)


class TestBaseAPIExtractor(unittest.TestCase):
    def test_abc_method(self):
        class TestBaseClass(BaseAPIExtractor):
            pass

        with self.assertRaises(TypeError):
            TestBaseClass()


class TestGeminiAPIExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = GeminiAPIExtractor()

    def test_extract_data_success(self):
        expected_output = "123.45"
        data_input = json.dumps({
            "events": [
                {"price": "123.45"}
            ]
        })

        output = self.extractor.extract_data(data_input)
        self.assertEqual(output, expected_output)

    def test_extract_invalid_data(self):
        invalid_input = "youfoundme"

        with self.assertRaises(ValueError):
            self.extractor.extract_data(invalid_input)

    def test_extract_data_missing_price(self):
        input_data = json.dumps({"events": [{}]})
        with self.assertRaises(ValueError):
            self.extractor.extract_data(input_data)


class TestGetExtractorClass(unittest.TestCase):
    def test_get_extractor_class(self):
        self.assertEqual(get_extractor_class("gemini"), GeminiAPIExtractor)

    def test_get_extractor_unknown_class(self):
        service = "koda"

        with self.assertRaises(KeyError) as context:
            get_extractor_class(service)

        self.assertIn(f"Unknown method {service}. Supported api services are", str(context.exception))
