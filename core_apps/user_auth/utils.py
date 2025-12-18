import random
import string

def generate_otp(length=6) -> str:
    
    digits = []  # make an empty list to hold numbers

    for _ in range(length):  
        number = random.randint(0, 9) # get a random number between 1 and 9
        digits.append(str(number))     # convert it to string and add to the list

    code_str = ''.join(digits)  # join all the strings together (e.g. ["4","7","2","8"] → "4728")
    return code_str
    
### THE ABOVE IS MY APPROACH FOR GENERATING RANDOM OTP'S AND BELOW IS THE ONE WRITTEN BY INSTRUCTOR, I HAVE GONE FOR MINE

# return "".join(random.choices(string.digits, k=length))   --- THE ONE BY INSTRUCTOR



# The logic outcome and the return type are the same in both approaches. In both cases, you generate length random digits, convert them into a single string, and return that string as the OTP. From the
# outside (how the function behaves and what it returns), there is no difference at all.
# The only difference is how the logic is written internally. Your version is more explicit and readable, while the one-liner is more compact. Functionally and in terms of return type (str), randomness,
# and OTP validity, both are equivalent.
# In short, there is no difference at all, other than how the code is written (style and readability).
