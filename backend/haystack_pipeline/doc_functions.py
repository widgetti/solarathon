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
        message = f'{filename} not deleted.  {error} [{lineno} in {filename}].'
        print(message)
    
def parse_retriever_doc(doc):
    pattern = r'\nQuestion\s*:\s*(.*?)\s*;\s*Answer\s*:\s*(.*?)\s*\n'
    result_dict = dict()
    match = re.search(pattern, doc.content, re.IGNORECASE)

    if match:
        question = match.group(1)
        answer = match.group(2)

        result_dict = {'Question': question, 'Answer': answer}
    # print(f'doc.meta keys: {doc.meta.keys()}')
    if 'integrations' in [key.lower() for key in doc.meta.keys()]:
        result_dict['Integrations'] = doc.meta.get('integrations', 'key not found')
        if result_dict['Integrations'] == doc.meta.get('Integrations', 'key not found'):
            result_dict['Integrations'] = None
    if 'category' in [key.lower() for key in doc.meta.keys()]:
        result_dict['Category'] = doc.meta.get('category', 'key not found')
        if result_dict['Category'] == doc.meta.get('Category', 'key not found'):
            result_dict['Category'] = None
    return result_dict

def list_retriever_results(retriever_results, show_score=False):
    """
    Function to convert Haystack results into a list of dictionaries containing 
    the question and answer sets and other attributes.

    Parameters
    ----------
    - retriever_results : Results from `retriever.run_query()`
    - show_score : show the confidence score of the model that retrieved it or the embedding created for it during indexing.
        https://docs.haystack.deepset.ai/docs/documents_answers_labels#document

    Returns
    -------
    results : list
        List of dictionaries containing the question and answer sets.
    """
    results = []
    for doc in retriever_results[0]['documents']:
        if show_score:
            results.append({
                **parse_retriever_doc(doc), 
                **{'Relevance Score': doc.score}
                })
        else:
            results.append(parse_retriever_doc(doc))
    return results