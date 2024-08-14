from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for rendering plots
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

data = {
    "Candidate sourced": 1200,
    "TA team shortlist": 800,
    "Shared with HM": 500,
    "Shortlisted by HM": 322,
    "Total L1 interview": 262,
    "Total L2 Interview": 62,
    "Total Bi Interview": 24,
    "offer declined": 5,
    "offer Extended": 18,  # Added this field
    "Joiner": 13
}

def reverse_funnel_calculation(joiners):
    percentage_reference = {
        "Candidate sourced": data["Candidate sourced"] / data["Joiner"],
        "TA team shortlist": data["TA team shortlist"] / data["Joiner"],
        "Shared with HM": data["Shared with HM"] / data["Joiner"],
        "Shortlisted by HM": data["Shortlisted by HM"] / data["Joiner"],
        "Total L1 interview": data["Total L1 interview"] / data["Joiner"],
        "Total L2 Interview": data["Total L2 Interview"] / data["Joiner"],
        "Total Bi Interview": data["Total Bi Interview"] / data["Joiner"],
        "offer declined": data["offer declined"] / data["Joiner"],
        "offer Extended": data["offer Extended"] / data["Joiner"],  # This line was added
        "Joiner": 1
    }

    result = {}
    for stage in data:
        result[stage] = int(round(joiners * percentage_reference[stage]))

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    joiners = int(request.form['joiners'])
    reversed_data = reverse_funnel_calculation(joiners)

    stages = list(reversed_data.keys())
    counts = list(reversed_data.values())

    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")
    palette = sns.color_palette("coolwarm", len(stages))
    bars = plt.barh(stages, counts, color=palette, edgecolor='black')

    for bar in bars:
        width = bar.get_width()
        plt.text(width + 5, bar.get_y() + bar.get_height() / 2, f'{width}',
                 va='center', ha='left', fontsize=10, color='black')

    plt.xlabel('Count', fontsize=14, fontweight='bold')
    plt.ylabel('Stage', fontsize=14, fontweight='bold')
    plt.title('Reverse Funnel Chart', fontsize=16, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({'reversed_data': reversed_data, 'plot_url': f'data:image/png;base64,{plot_url}'})

if __name__ == '__main__':
    app.run(debug=True)
