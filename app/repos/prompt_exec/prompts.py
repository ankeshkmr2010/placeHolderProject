class Prompts:
    JD_EXTRACTION_PROMPT = """
        You are a helpful assistant to  a hiring manager. Your task is to extract concise key criteria from a job description.
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
    RESUME_PROCESSING_PROMPT = "Evaluate the following resume against the criteria: {criteria}\n\nResume:\n{resume}"
