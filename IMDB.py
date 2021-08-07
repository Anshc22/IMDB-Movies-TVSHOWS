# Add more urls for scraping if you like, most likely should work unless IMDB changes their HTML structure

urls=["https://www.imdb.com/chart/top",
             "https://www.imdb.com/chart/moviemeter",
             "https://www.imdb.com/chart/top-english-movies",
             "https://www.imdb.com/chart/bottom",
             "https://www.imdb.com/india/top-rated-indian-movies",
             "https://www.imdb.com/chart/tvmeter",
            "https://www.imdb.com/chart/toptv"]

info=[]
def parse(url):
    
    sheet_name=url[url.find("/",url.find(".com")+5)+1:]       
    r=requests.get(url)
    soup=bs(r.content,"html.parser")
    titles=soup.find_all("td",{"class":"titleColumn"})
    ratings=[float(rating.text) for rating in soup.find_all("strong")]
    for title,rating in zip(titles,ratings):
        link="https://www.imdb.com/"+title.a["href"]
        Title=title.a.text
        try:
            director_raw=title.a["title"]
            director=director_raw[:director_raw.find("(")-1]
        except:
            director=""
        Year=int(title.span.text[1:5])
        movie={"Title":Title,"Rating":rating,"Year":Year,"Director":director,"URL":link}
        info.append(movie)
    
    

for url in urls:
    parse(url)
    # Tweak this accordingly
    time.sleep(1.5)

df=pd.DataFrame(info)

# Segregating data into Movies(Lowest and Topmost), Top Rated Indian Movies and TV SHOWS(Most Popular and Top Rated)
english_moviesdf=df.iloc[:684]
indiandf=df.iloc[684:934]
tvdf=df.iloc[934:]



with pd.ExcelWriter("IMDB.xlsx") as writer:
    
    
    english_moviesdf.drop_duplicates(subset="Title").sort_values("Rating",ascending=False).to_excel(writer,sheet_name="All Movies",index=False)
    indiandf.sort_values("Rating",ascending=False).to_excel(writer,sheet_name="Indian Movies",index=False)
    tvdf.drop_duplicates(subset="Title").sort_values("Rating",ascending=False).to_excel(writer,sheet_name="TV Shows",index=False)
