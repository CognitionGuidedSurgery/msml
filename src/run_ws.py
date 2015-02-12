__author__ = 'weigl'

if __name__ == '__main__':
    from msmllab.rest import app
    app.run(debug=True, host="0.0.0.0", port=8522)