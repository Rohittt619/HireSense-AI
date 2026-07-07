import plotly.express as px


class Visualizer:

    @staticmethod
    def chart(skills):

        matched = len(skills["matched"])

        missing = len(skills["missing"])

        fig = px.pie(

            values=[matched, missing],

            names=["Matched", "Missing"],

            title="Skill Match Analysis"

        )

        fig.update_traces(textinfo="percent+label")

        return fig