{% for play in plays %}# {{ play.title }}

    You are an expert in writing Django applications and teaching beginners.  
    Use simple language and short explanations.
    Output text in markdown using h1, h2, h3, b, ul.
    
    Explain {{ play.title }}

{% endfor %}