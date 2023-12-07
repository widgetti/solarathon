

def cat2path( category : str):
    return category.replace(' ','-').replace("\\",'-').replace("/",'-').lower()