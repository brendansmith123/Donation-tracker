from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os
app = Flask(__name__)
uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/DonationTracker')#DonationTracker 
client = MongoClient(uri)
db = client.get_default_database()

donations = db.donations
charities=db.charities


@app.route('/')
def donations_index():
    '''Show all donations.'''
    return render_template('donations_index.html', donations=donations.find())

@app.route('/donations/new')
def donation_recent():
    return render_template('donations_new.html')

@app.route('/donations/create', methods=['POST'])
def donation_applied():
    print(request.form.get('name'))
    donation = {
        'name': request.form.get('name'),
        'amount': request.form.get('amount'),
        'rating': request.form.get('rating'),
        'description': request.form.get('description'),
        'date': datetime.datetime.now()
      }
    donation_id=donations.insert_one(donation).inserted_id
    return redirect(url_for('donation_show',donation_id=donation_id))

@app.route('/donations/<donation_id>')
def donation_show(donation_id):
    current_donation=donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_show.html', donation=current_donation)

@app.route('/donations/<donation_id>/remove', methods=['POST'])
def donation_removed(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('donations_index'))

# charity index
@app.route('/charities')
def charities_index():
  return render_template('charity_index.html', charities=charities.find())

@app.route('/charities/new', methods=['POST'])
def charities_new():
  return render_template('add_charity.html')


@app.route('/charities', methods=['POST'])
def charity_submit():
  charity = {
    'charity_name': request.form.get('charity_name'),
  }

  charities.insert_one(charity)
  return redirect(url_for('charity_index'))


@app.route('/charities/<charity_name>')
def charity_profile(charity_name):
  charity = charities.find_one({'name': charity_name})
  return render_template('add_charity.html', charity=charity, donations = donations.find({'charity_name': charity_name}))


@app.route('/charities/<charity_name>', methods=['POST'])
def charities_update(charity_name):
  updated_charity = {
    'name': request.form.get('charity_name'),
  }
  charities.update_one(
    {'name': charity_name},
    {'$set': updated_charity}
  )



if __name__ == '__main__':
  app.run(debug=True)