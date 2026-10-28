class Solution {
    public int reverse(int x) {
        int result = 0;

        while (x != 0) {

            int digit = x % 10;
            x = x / 10;

            // Check for positive overflow
            if (result > Integer.MAX_VALUE / 10 ||
                (result == Integer.MAX_VALUE / 10 && digit > 7)) {
                return 0;
            }

            // Check for negative overflow
            if (result < Integer.MIN_VALUE / 10 ||
                (result == Integer.MIN_VALUE / 10 && digit < -8)) {
                return 0;
            }

            result = result * 10 + digit;
        }

        return result;
    }
}
    
