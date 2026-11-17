from app.core import split_text, Retriever, evidence_answer

def test_chunks_overlap_and_metadata():
    chunks = split_text('abcdefghi', 'sample.pdf', 2, size=5, overlap=2)
    assert [c.text for c in chunks] == ['abcde', 'defgh', 'ghi']
    assert all(c.page == 2 for c in chunks)

def test_retrieval_and_citations():
    index = Retriever()
    index.add(split_text('The refund policy lasts thirty days.', 'policy.pdf', 1))
    results = index.search('refund policy')
    assert results and results[0]['source'] == 'policy.pdf'
    assert '[policy.pdf, page 1]' in evidence_answer('refund?', results)

def test_empty_index_abstains():
    assert 'could not find' in evidence_answer('anything', []).lower()
