"""11.6 export scope guards; native evidence is recorded separately."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'engine'))
import native_export as export

PROFILE = 'jy14-headless-macos-11.6.0'


class ExportScope116Tests(unittest.TestCase):
    def fixture(self):
        return {'materials': {'videos': [{'type': 'video'}]}, 'tracks': [
            {'type': 'video', 'segments': [{}]},
            {'type': 'text', 'segments': [{}]},
            {'type': 'audio', 'segments': [{'common_keyframes': [{'property_type': 'KFTypeVolume'}]}]}]}

    def test_basic_video_static_text_and_audio_curves_are_allowed(self):
        value = self.fixture()
        before = deepcopy(value)
        export.validate_116_scope(value, PROFILE)
        self.assertEqual(value, before)

    def test_untested_effects_and_compounds_fail_before_rendering(self):
        for bucket in ('drafts', 'common_mask', 'transitions', 'video_effects', 'effects'):
            with self.subTest(bucket=bucket):
                value = self.fixture()
                value['materials'][bucket] = [{}]
                with self.assertRaisesRegex(ValueError, bucket):
                    export.validate_116_scope(value, PROFILE)

    def test_image_and_gif_materials_are_not_silently_allowed(self):
        for kind in ('photo', 'gif', None):
            with self.subTest(kind=kind):
                value = self.fixture()
                value['materials']['videos'][0]['type'] = kind
                with self.assertRaisesRegex(ValueError, 'image/GIF'):
                    export.validate_116_scope(value, PROFILE)

    def test_picture_and_text_curves_are_not_claimed_from_audio_evidence(self):
        for track in (0, 1):
            value = self.fixture()
            value['tracks'][track]['segments'][0]['common_keyframes'] = [{}]
            with self.assertRaisesRegex(ValueError, 'keyframe'):
                export.validate_116_scope(value, PROFILE)

    def test_existing_115_scope_is_unchanged(self):
        export.validate_116_scope({'materials': {'drafts': [{}]}}, 'jy14-headless-macos-11.5.0')


if __name__ == '__main__':
    unittest.main()
