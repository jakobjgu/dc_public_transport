include .env
export

.PHONY : quick_test staging transformation marts test-staging test-transformation test-marts streamlit_viz docs docs_serve dbt_clean dbt_debug

DBT_FOLDER = metro_analytics_dbt
DBT_TARGET = dev

staging:
	cd $(DBT_FOLDER) && \
	dbt run --selector staging --target $(DBT_TARGET)

quick_test:
	cd $(DBT_FOLDER) && \
	dbt run --select stg_ridership_weekday --target $(DBT_TARGET)

streamlit_viz:
	streamlit run visualizations/streamlit_app.py

streamlit_viz_ec2:
	streamlit run visualizations/streamlit_app.py --server.address=0.0.0.0 --server.port=8501

docs:
	cd $(DBT_FOLDER) && \
	dbt docs generate --target $(DBT_TARGET)

docs_serve:
	cd $(DBT_FOLDER) && \
	dbt docs serve --target $(DBT_TARGET)

dbt_clean:
	cd $(DBT_FOLDER) && \
	dbt clean

dbt_debug:
	cd $(DBT_FOLDER) && \
	dbt debug --target $(DBT_TARGET)

full_pipeline:
	cd $(DBT_FOLDER) && \
	dbt clean && \
	dbt deps && \
	dbt run --selector base --target $(DBT_TARGET) && \
	dbt run --selector staging --target $(DBT_TARGET) && \
	dbt run --selector marts --target $(DBT_TARGET) && \
	dbt test --target $(DBT_TARGET) && \
	dbt docs generate --target $(DBT_TARGET)

duck:
	duckdb metro_analytics_dbt/dev.duckdb