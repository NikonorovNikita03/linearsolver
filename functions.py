def get_settings():
    with open("settings.txt") as f:
        settings = f.read()
        
    try:
        lines = settings.strip().split('\n')
        result = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = int(value.strip())
        return result
    except:
        return {
            "size_x": 4,
            "size_y": 4,
            "width": 1366,
            "height": 768
        }
    
def combine_arrays_pure(arr1, arr2):
    rows1, cols1 = len(arr1), len(arr1[0]) if arr1 else 0
    rows2, cols2 = len(arr2), len(arr2[0]) if arr2 else 0
    
    if rows1 > rows2 or cols1 > cols2:
        return arr1
    
    result = [row.copy() for row in arr2]
    
    for i in range(rows1):
        for j in range(cols1):
            result[i][j] = arr1[i][j]
    
    return result

def combine_arrays_1d_pure(arr1, arr2):
    len1, len2 = len(arr1), len(arr2)
    
    if len1 >= len2:
        return arr1
    
    result = arr1.copy() + arr2[len1:]
    
    return result

def str_to_number(s):
    try:
        f = float(s)
        return int(f) if f.is_integer() else f
    except:
        return 0