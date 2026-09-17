import streamlit as st
from recommendation_mcp.graph.workflow import build_graph
import asyncio
st.set_page_config(
    page_title="ChefPal",

)

st.title("ChefPal")
st.write("Nutrition and meal recommendation system")
query = st.text_input(
    "What kind of meal are you looking for?",
    placeholder="e.g. chicken dinner under 500 calories",
)

if query:
    st.write("Your request:", query)


if st.button("Get recommendations"):
    if not query:
        st.warning("Please enter a meal request.")
    else:
        graph = build_graph()

        result = asyncio.run(
            graph.ainvoke(
                {
                    "user_query": query,
                    "meal_request": None,
                    "retrieval_result": None,
                    "ranking_result": None,
                }
            )
        )

        retrieval_result = result["retrieval_result"]
        ranking_result = result["ranking_result"]

        recipes_by_id = {
            recipe.recipe_id: recipe.recipe
            for recipe in retrieval_result.candidates
        }

        st.subheader("Recommendations")

        if not ranking_result.recommendations:
            st.info(
                "No recipes matched your request. "
                "Try changing your dietary preferences or calorie limit."
            )
        else:
            for recommendation in ranking_result.recommendations:
                recipe = recipes_by_id[recommendation.recipe_id]

                st.subheader(recipe["name"])

                col1, col2 = st.columns([1, 2])

                with col1:
                    if recipe["image_path"]:
                        st.image(recipe["image_path"], width=180)

                with col2:
                    st.write(
                        f"**{recipe['calories_kcal']:.1f} kcal** · "
                        f"**{recipe['minutes']} min** · "
                        f"\u2b50 **{recipe['rating']:.2f}**"
                    )

                    st.write(recipe["description"])

                    st.caption(recommendation.reason)

                with st.expander("View recipe"):
                    st.markdown("**Ingredients**")

                    for ingredient in recipe["ingredients"]:
                        st.write(f"- {ingredient}")

                    st.markdown("**Instructions**")

                    for number, step in enumerate(recipe["steps"], start=1):
                        st.write(f"{number}. {step}")

                st.divider()