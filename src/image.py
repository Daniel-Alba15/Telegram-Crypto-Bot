import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
from datetime import datetime
import pytz


class Image():
    def __init__(self):
        self.image_b64 = None

    def get_image(self):
        if not self.image_b64:
            raise AttributeError("There isn't a generated report")

        return self.image_b64

    def generate_report(self, coins, prices, have):
        data = {"coins": coins, "prices": prices, "have": have}
        df = pd.DataFrame(data)

        plt.ylim([min(prices) - 1, max(prices) + 1])
        d_now = datetime.now(pytz.timezone("America/Bogota")).strftime("%d/%m/%Y, %H:%M")
        plt.title(d_now)

        plt.bar(df["coins"], df["prices"], facecolor="#9999ff")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        self.image_b64 = base64.b64encode(image_png).decode("utf-8")
        buffer.close()
