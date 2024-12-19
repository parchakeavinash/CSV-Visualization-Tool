from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly.express as px
import io
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Basic route for the homepage
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visualize Your CSV Data</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f0f2f5;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 600px;
                width: 90%;
            }
            h1 {
                color: #2e7d32;
                font-size: 28px;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                font-size: 16px;
                margin-bottom: 40px;
            }
            .features {
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
            }
            .feature {
                display: flex;
                flex-direction: column;
                align-items: center;
                color: #2e7d32;
            }
            .feature i {
                font-size: 24px;
                margin-bottom: 10px;
            }
            .feature-text {
                font-size: 14px;
                color: #666;
            }
            .upload-section {
                margin: 30px 0;
            }
            .file-input-wrapper {
                margin-bottom: 15px;
            }
            .choose-file-btn {
                background-color: white;
                border: 2px solid #2e7d32;
                color: #2e7d32;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s;
            }
            .choose-file-btn:hover {
                background-color: #f0f7f0;
            }
            .visualize-btn {
                background-color: #2e7d32;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s;
            }
            .visualize-btn:hover {
                background-color: #1b5e20;
            }
            .footer {
                margin-top: 30px;
                color: #666;
                font-size: 14px;
            }
            input[type="file"] {
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Visualize Your CSV Data</h1>
            <p class="subtitle">Transform your boring spreadsheets into beautiful, insightful visualizations in just a few clicks.</p>
            
            <div class="features">
                <div class="feature">
                    <i class="fas fa-chart-line"></i>
                    <span class="feature-text">Interactive Charts</span>
                </div>
                <div class="feature">
                    <i class="fas fa-upload"></i>
                    <span class="feature-text">Easy Uploads</span>
                </div>
                <div class="feature">
                    <i class="fas fa-download"></i>
                    <span class="feature-text">Quick Downloads</span>
                </div>
            </div>

            <form action="/visualize" method="post" enctype="multipart/form-data" class="upload-section">
                <div class="file-input-wrapper">
                    <label for="file-upload" class="choose-file-btn">
                        <i class="fas fa-file-upload"></i> Choose File
                    </label>
                    <input id="file-upload" type="file" name="file" accept=".csv" required>
                </div>
                <button type="submit" class="visualize-btn">Visualize Now</button>
            </form>

            <div class="footer">
                Powered by AvinashParchake
            </div>
        </div>

        <script>
            // Display selected filename
            document.getElementById('file-upload').addEventListener('change', function() {
                const fileName = this.files[0].name;
                this.previousElementSibling.textContent = fileName;
            });
        </script>
    </body>
    </html>
    '''

# Route for handling file upload and visualization
@app.route('/visualize', methods=['POST'])
def visualize():
    try:
        file = request.files['file']
        if not file:
            return 'No file uploaded', 400

        # Read CSV
        df = pd.read_csv(file)
        
        # Create visualization
        fig = px.line(df, x='Date', y=['Sales', 'Profit'], title='Sales and Profit Over Time')
        
        # Convert to HTML
        plot_html = fig.to_html(full_html=False, include_plotlyjs=True)
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Visualization Result</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: Arial; padding: 20px; text-align: center; }}
                .container {{ max-width: 1000px; margin: 0 auto; }}
                .btn {{ padding: 10px 20px; background: #4CAF50; color: white; 
                       border: none; cursor: pointer; text-decoration: none; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Visualization Results</h2>
                {plot_html}
                <br><br>
                <a href="/" class="btn">Back to Upload</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)