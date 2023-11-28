import unittest
from Fishing import FishingGame, hash_password 


class TestFishingGame(unittest.TestCase):

    def test_roll_dice(self):
        """Test if roll_dice returns a number between 1 and 6."""
        result = FishingGame.roll_dice()
        self.assertIn(result, range(1, 6))

    def test_get_catch(self):
        """Test if get_catch returns the correct fish name for a given dice roll."""
        # Adjust the dice roll value to match the expected fish name
        dice_roll_value = 1  # Update this value based on your fish_mapping data
        expected_fish_name = "King George Whiting"  # Update this based on the correct mapping
        fish_name = FishingGame.get_catch(dice_roll_value)
        self.assertEqual(fish_name, expected_fish_name)

    def test_calculate_score(self):
        """Test score calculation for keeping and releasing a fish."""
        # Assuming 'FishName' is a valid fish with known points
        score_kept = FishingGame.calculate_score('FishName', True)
        score_released = FishingGame.calculate_score('FishName', False)
        self.assertIsInstance(score_kept, int)
        self.assertIsInstance(score_released, int)
        # Add more assertions as needed based on your scoring logic

class TestPasswordHashing(unittest.TestCase):

    def test_password_hashing(self):
        """Test if the password is correctly hashed."""
        password = "testpassword"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)
        self.assertNotEqual(hashed1, hashed2)  # Hashes should differ due to salt

    def test_hash_length(self):
        """Test if the hash length is as expected."""
        password = "Password"
        hashed = hash_password(password)
        self.assertEqual(len(hashed), 64)  


if __name__ == '__main__':
    unittest.main()