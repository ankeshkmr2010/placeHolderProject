class Prompts:
    JD_EXTRACTION_PROMPT = """
        You are a helpful assistant to  a hiring manager.
        Your task is to extract concise key criteria from a job description.
        You should extract a list of one line requirements and criterion for the job description provided.
        The extracted criteria will be used to evaluate the resumes against the job description.
        
        Make sure to extract the criteria in a concise manner, and avoid any unnecessary details.
        The criteria should be along the lines of:
        - Skill requirements
        - Experience
        - Educational qualifications
        - Certifications
        - Explicit requirements mentioned in the job description
        
        Rank the criteria based on their importance to the job role. Make sure to list the most relevant criteria first.
        
        Try to keep the list concise.
        Avoid repeating similar criteria.
        
        Job description : 
        {{ jd_text }}
    
    """
    RESUME_PROCESSING_PROMPT = """
    You are a helpful assistant to  a hiring manager.
    You are given a list of criteria extracted from a job description.
    Your task is to evaluate the resumes against these criteria.
    Make sure to evaluate each resume against the criteria provided.
    Provide a score for each resume based on how well it matches the criteria.
    The score should be between 0 and 5, where 0 means no match and 5 means perfect match.
    The criteria are as follows:
    {{ criteria }}
    
    Evaluate the following resume against the criteria provided.
    Resume:\n {{ resume }}
    """
