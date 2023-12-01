import os
import sys
import json
import re
def delete_documents(filename, filepath):
    """Function to delete files prior to their generation."""
    if filepath:
        filename = f'{filepath}/{filename}'
    try:
        os.remove(filename)
        print(f'{filename} deleted')
    except Exception as error:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        message = f'{filename} not deleted. An error occurred on line {lineno} in {filename}: {error}.'
        print(message)

def haystack_doc_to_dict(input_string):
    # Define a regular expression pattern
    pattern = r'\nQuestion\s*:\s*(.*?)\s*;\s*Answer\s*:\s*(.*?)\s*\n'

    # Search for matches using the pattern
    match = re.search(pattern, input_string)

    # Check if a match is found
    if match:
        # Extract the captured groups (Question and Answer)
        question = match.group(1)
        answer = match.group(2)

        # Create and return a dictionary
        result_dict = {'Question': question, 'Answer': answer}
        return result_dict
    else:
        return None


def list_retriever_results(retriever_results):
    """
    
    """
    results = []
    for doc in retriever_results[0]['documents']:
        results.append(haystack_doc_to_dict(doc.content))
    return results