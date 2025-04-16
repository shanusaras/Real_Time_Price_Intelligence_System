# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import sys
print("DEBUG: CWD =", os.getcwd())
print("DEBUG: sys.path =", sys.path)
print("DEBUG: __file__ =", __file__)
with open(__file__, 'r', encoding='utf-8') as f:
    print("DEBUG: First 10 lines of file:")
    for i, line in enumerate(f):
        if i >= 10: break
        print(line.rstrip())

def test_isolated():
    try:
        print("This is an isolated test. No project code is run.")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_isolated()
