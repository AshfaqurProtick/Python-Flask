from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query

app= Flask(__name__)
api= Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db' # name of the database
# 'sqlite:///tmp/database.db' creates a temp file in the current directory
db= SQLAlchemy(app)

class VideoModel(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    views= db.Column(db.Integer, nullable=False)
    likes=db.Column(db.Integer, nullable=False)

    # __repr__()  returns a printable representation of the object. __repr__() is more useful for developers while __str__() is for end users.
    def __repr__(self):
        return f"Video(name= {self.name}, views= {self.views}, likes= {self.likes}"

# db.create_all()

video_put_args= reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

video_update_args= reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes of the video is required")

# decorator style 
# The decorator marshal_with is what actually takes your data object and applies the field filtering.
# The marshalling can work on single objects, dicts, or lists of objects.
resource_fields= {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields) # python decorator with decorator library (marshel_with)
    def get(self, video_id):
        result= VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that ID")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        '''Make new object in database'''
        args= video_put_args.parse_args()
        result= VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ID taken...")
        video= VideoModel(id=video_id, name=args['name'], views= args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201 # 201 means Created

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args= video_update_args.parse_args()
        result= VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesnt exist, cant update")

        if args['name']:
            result.name= args['name']
        if args['views']:
            result.views= args['views']
        if args['likes']:
            result.likes= args['likes']

        db.session.commit()
        
        return result


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    # starting flask server
    app.run(debug=True) # dont run debug mode in production phase, only in developement phase

