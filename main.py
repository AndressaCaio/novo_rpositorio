from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2] or "N/A",
        "duration": all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/like")
def liked_movie():
    global all_movies
    movie_data=assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# api para retornar a lista de filmes curtidos
@app.route("/liked",methods = ["GET"])
def liked():
    global liked_movie
    return jsonify({
        "data": liked_movies,
        "status": "success"
    })

@app.route("/dislike")
def unliked_movie():
    global all_movies

    movie_data=assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies

    movie_data=assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

# api para retornar a lista de filmes populares
@app.route("/pupular_movies")
def popular_movies():
    popular_movie_data = []
    for index,row in autput.iterrows():
        _p = {
            "original_title": row["original_title"],
            "poster_link":  row["poster_link"],
            "release_date": row["release_date"] or "n/a",
            "duration": row["runtime"],
            "rating":   row["weighted_rating"]/2
        }
        popular_movie_data.append(_p)
    return jsonify({
        "data": popular_movie_data,
        "status": "success"
    })    
# api para retornar a lista de filmes recomendados
@app.route("/recommended_movies")
def recommended_movies():
    global liked_movies
    col_names = ["original_title","poster_link","release_date","run_time","weighted_rating"]
    all_recomended = pd.dataframe(colunms = col_names)
    for liked_movie in liked_movies:
        autput = get_recommendations(liked_movie["original_title"])
        all_recomended = all_recomended.append(autput)
    all_recomended.drop_duplicates(subset = ["original_title"],inplace = True)
    recomended_movie_data = []
    for index_row in all_recomended.iterrows():
        _p = {
            "original_title": row["original_title"],
            "poster_link":  row["poster_link"],
            "release_date": row["release_date"] or "n/a",
            "duration": row["runtime"],
            "rating":   row["weighted_rating"]/2
        }
        popular_movie_data.append(_p)
    return jsonify({
        "data": popular_movie_data,
        "status": "success"
    })    
if __name__ == "__main__":
  app.run()
