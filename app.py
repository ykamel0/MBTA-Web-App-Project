import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
import mbta_helper

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place = request.form.get("place")

        if not place:
            return render_template("index.html", error="Please provide a valid place name.")

        try:
            station_name, wheelchair_accessible = mbta_helper.find_stop_near(place)

            latitude, longitude = mbta_helper.get_lat_lng(place)

            return render_template(
                "index.html",
                longitude=longitude,
                latitude=latitude,
                station_name=station_name,
                wheelchair_accessible=wheelchair_accessible,
                mapbox_api_key=os.getenv("MAPBOX_API_KEY")
            )
        except Exception as e:
            return render_template("index.html", error="Could not find location. Please try again.")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)