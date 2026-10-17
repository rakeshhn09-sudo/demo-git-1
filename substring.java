class Solution {
    public int lengthOfLongestSubstring(String s) {
         String result = "";
        int maxLength = 0;

        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);

            int index = result.indexOf(ch);

            if (index != -1) {
                result = result.substring(index + 1);
            }

            result = result + ch;
            maxLength = Math.max(maxLength, result.length());
        }

        return maxLength;
    }
}