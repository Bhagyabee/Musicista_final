from flask import Blueprint , jsonify,redirect,render_template,url_for , request
from flask_login import login_required,current_user
import  stripe
import json
from flask_mail import Mail , Message
from flask import  jsonify
from musicista.preprocess import preprocess_audio
import numpy as np
from tensorflow.keras.models import load_model



from flask import request,jsonify
from musicista.chat import get_response
views = Blueprint('views',__name__)
model = load_model(r"C:\Users\BHAGYABEE\OneDrive\Desktop\test\musicista\music_genre_model.h5")

genre_mapping = {
    'pop': ['Artist1', 'Artist2', 'Artist3'],
    'rock': ['Artist4', 'Artist5', 'Artist6'],
    'hip-hop': ['Artist7', 'Artist8', 'Artist9'],
    # Add more genres and artists as needed
}

# @views.route('/get_recommendations')


@views.route('/')
@login_required
def home():
    return render_template('login.html',user=current_user)

@views.route('/landing',methods =['GET'])
def landing():
    return render_template('index.html',user= current_user)

@views.route('/artists', methods=['GET'])
def artists():
    return render_template('ArtistSelection.html',user=current_user)
@views.route('/artistbooking', methods=['GET'])
def artistbooking():
    return render_template('artistbooking.html',user=current_user)

@views.route('/artistsSolo', methods=['GET'])
def artistsSolo():
    return render_template('solo.html',user=current_user)

@views.route('/artistsDuet', methods=['GET'])
def artistsDuet():
    return render_template('duet.html',user=current_user)
# @views.route('/stripe_pay')
# def index():
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price': 'price_1O03qnSAm1yXJy6FP8bV5LxP',
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
#         cancel_url=url_for('stripe', _external=True),
#     )
#     return  render_template('stripe.html',
#                             checkout_session_id=session['id'],
#                             checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
#                             )



@views.route('/thanks',methods =['GET','POST'])
def thanks():

  return render_template('thanks.html')
@views.route('/book-now',methods =['GET','POST'])
def book():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1O03qnSAm1yXJy6FP8bV5LxP',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('views.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('views.sstripe', _external=True),
    )
    return  render_template('payment.html',user=current_user,
                            checkout_session_id=session['id'],
                            checkout_public_key='pk_test_51O03ftSAm1yXJy6FXwURoEWIig94zvLUQG2UEmLhq9UogQ9ipcKJcjlaBVb7sJSeoRBn5Dg7Ghnu8zBEqwdG3IEt0017SqYlZK'
                            )


@views.route('/book',methods = ['GET','POST'])
def sstripe():
    return render_template('stripe.html',user=current_user)
@views.route('/payment',methods =['POST'])
def payment():
    return render_template('payment.html',user=current_user)

@views.route('/chat')
def chat():
    return render_template('chatbot.html')

@views.route('/predict',methods =['POST'])
def predict():
    text = request.get_json().get("message")

    response = get_response(text)
    message = {"answer": response}
    return  jsonify(message)

@views.route('/genre')
def index():
    return render_template('genre.html')


@views.route('/predict_genre', methods=['POST'])
def predict_genre():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    response ={}

    try:
        # Preprocess the audio file
        processed_data = preprocess_audio(file)
        # Reshape the data to match the expected input shape of your model
        processed_data = np.expand_dims(processed_data, axis=0)

        # Make the prediction
        prediction = model.predict(processed_data)
        predicted_genre = np.argmax(prediction)

        # Map the genre index to the corresponding label
        genre_labels = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
        predicted_genre_label = genre_labels[predicted_genre]

        if predicted_genre_label.lower() in genre_mapping:
            recommended_artists = genre_mapping[predicted_genre_label.lower()]
        else:
            recommended_artists = ["No recommendations available for this genre."]

        response = {
            'predicted_genre': predicted_genre_label,
            'recommended_artists': recommended_artists,

        }
        response ={
            'redirect_url': url_for('views.prediction_result', response=json.dumps(response))
        }

        return jsonify(response)

        # return jsonify({'predicted_genre': predicted_genre_label})

    except Exception as e:
        return jsonify({'error': str(e)})

@views.route('/prediction_result/<response>', methods=['GET','POST'])
def prediction_result(response):
    # Parse the JSON response
    response_data = json.loads(response)

    # Render the prediction result page with the data
    return render_template('prediction_result.html', response_data=response_data)





























