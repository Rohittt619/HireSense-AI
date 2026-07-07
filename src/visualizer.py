import plotly.graph_objects as go
import plotly.express as px


class Visualizer:

    @staticmethod
    def pie_chart(skills):

        labels = ["Matched Skills", "Missing Skills"]

        values = [
            len(skills["matched"]),
            len(skills["missing"])
        ]

        fig = px.pie(
            names=labels,
            values=values,
            hole=0.55,
            title="Skill Match Analysis"
        )

        return fig

    @staticmethod
    def score_chart(ats, similarity, skill_score):

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=["ATS", "Similarity", "Skill Match"],
                y=[ats, similarity, skill_score]
            )
        )

        fig.update_layout(
            title="Resume Performance",
            yaxis_range=[0,100]
        )

        return fig