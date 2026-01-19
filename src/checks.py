import pandas as pd
import numpy as np

from scipy.stats import chi2_contingency, pearsonr, zscore

class FairnessAudit:
    def __init__(self, data, target=None):
        """
        data: pandas DataFrame or path to CSV/XLSX
        target: όνομα target column (π.χ. "label")
        protected_attributes: λίστα προστατευμένων χαρακτηριστικών (π.χ. ["gender", "age_group"])
        """
        self.data = self._load_data(data)
        self.target = target.lower()
        self.protected_attributes = ['gender','gen','female','male','sex','country','region',
                                    'ethnicity','age','age_group','yo','years','years_old','birth_date','birthdate']

    def _load_data(self, data):
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, str):
            if data.endswith(".csv"):
                return pd.read_csv(data)
            if data.endswith(".xlsx"):
                return pd.read_excel(data)
        

    # ---------------------------
    # 1. Class Imbalance Analysis
    # ---------------------------
    def check_class_imbalance(self):
        if self.target is None:
            return {"error": "No target variable specified."}

        # Counts & percentages
        counts = self.data[self.target].value_counts(dropna=False)
        pct = counts / len(self.data)

        # Dominant class info
        dominant_class = counts.idxmax()
        dominant_pct = float(pct.max() * 100)
        imbalance = bool(dominant_pct > 80)

        # Summary text
        summary = (
            f"The target variable '{self.target}' has {len(counts)} unique classes. "
            f"The dominant class is '{dominant_class}', representing "
            f"{dominant_pct:.2f}% of the dataset. "
            f"{'This indicates a strong class imbalance.' if imbalance else 'No severe class imbalance detected.'}"
        )

        return {
            "counts": counts.to_dict(),
            "percentages": pct.round(4).to_dict(),
            "imbalance_flag": imbalance,
            "summary": summary
        }
    # ----------------------------------------
    # 2. Representation Issues / Group Presence
    # ----------------------------------------
    def check_representation(self):
        if self.target is None:
            return {"error": "No target variable specified."}

        results = {}
        summaries = []

        for attr in self.protected_attributes:
            if attr not in self.data.columns:
                continue

            counts = self.data[attr].value_counts(dropna=False)
            pct = counts / len(self.data)
            underrep = pct[pct < 0.05].index.tolist()

            results[attr] = {
                "counts": counts.to_dict(),
                "percentages": pct.round(4).to_dict(),
                "underrepresented_groups": underrep
            }

            if underrep:
                summaries.append(
                    f"In '{attr}', the following groups are underrepresented (<5%): {underrep}."
                )
            else:
                summaries.append(
                    f"All groups in '{attr}' are adequately represented."
                )

        if not results:
            return {
                "result": "No Demographic Columns Found",
                "summary": "No protected or demographic attributes were detected in the dataset."
            }

        return {
            "results": results,
            "summary": " ".join(summaries)
        }


    # --------------------------------------------
    # 3. Demographic Bias Detection in Target Label
    # --------------------------------------------
    def demographic_bias(self):
        if self.target is None:
            return {"error": "No target variable specified."}

        results = {}
        summaries = []

        for attr in self.protected_attributes:
            if attr not in self.data.columns:
                continue

            contingency_table = pd.crosstab(self.data[attr], self.data[self.target])
            chi2, p, _, _ = chi2_contingency(contingency_table)
            bias = p < 0.05

            results[attr] = {
            "contingency_table": contingency_table.to_dict(),
            "chi2_p_value": p,
            "bias_flag": bias
            }

            summaries.append(
            f"Demographic bias check for '{attr}': "
            f"{'bias detected' if bias else 'no statistically significant bias'} "
            f"(p-value = {p:.4f})."
            )

        if not results:
            return {
            "result": "No Demographic Columns Found",
            "summary": "No demographic attributes were available for bias testing."
            }

        return {
            "results": results,
            "summary": " ".join(summaries)
        }
    # ---------------------------------------------------
    # 4. Correlation of Features with Protected Attributes
    # ---------------------------------------------------
    def correlation_with_protected(self):
        results = {}
        summaries = []

        numeric_cols = self.data.select_dtypes(include=[np.number]).columns

        for p_attr in self.protected_attributes:
            if p_attr not in self.data.columns:
                continue
            if self.data[p_attr].dtype == "object":
                continue

            results[p_attr] = {}

            for col in numeric_cols:
                if col == p_attr:
                    continue
                try:
                    corr, p_value = pearsonr(
                        self.data[p_attr].dropna(),
                        self.data[col].dropna()
                    )
                    results[p_attr][col] = {
                        "correlation": corr,
                        "p_value": p_value
                    }

                    if abs(corr) > 0.7:
                        summaries.append(
                            f"Strong correlation detected between '{p_attr}' and '{col}' "
                            f"(corr={corr:.2f}, p={p_value:.4f})."
                        )
                except Exception:
                    pass

        if not results:
            return {
                "result": "No Demographic Columns Found",
                "summary": "No numeric demographic attributes were found for correlation analysis."
            }

        if not summaries:
            summaries.append("No strong correlations detected between protected attributes and numeric features.")

        return {
            "results": results,
            "summary": " ".join(summaries)
        }


class algorithmic_checks:
    def __init__(self, data):
        """
        data: pandas DataFrame or path to CSV/XLSX
        target: όνομα target column (π.χ. "label")
        protected_attributes: λίστα προστατευμένων χαρακτηριστικών (π.χ. ["gender", "age_group"])
        """
        self.data = self._load_data(data)
       
    def _load_data(self, data):
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, str):
            if data.endswith(".csv"):
                return pd.read_csv(data)
            if data.endswith(".xlsx"):
                return pd.read_excel(data)
    def overfitting_check(self):
        """
        Basic heuristic check for potential overfitting conditions:
        - Too many features compared to samples.
        - High correlation between features.
        """
        if self.data is None:
            raise ValueError("Data not loaded.")

        n_samples = int(self.data.shape[0])
        n_features = int(self.data.shape[1])

        feature_ratio = n_features / max(n_samples, 1)

        correlations = self.data.corr(numeric_only=True).abs()
        high_corr_pairs = int(
            np.sum((correlations > 0.9).values) - correlations.shape[0]
        )

        #  Heuristic flags
        ratio_flag = feature_ratio > 0.5
        correlation_flag = high_corr_pairs > 0

        #  Summary logic
        if not ratio_flag and not correlation_flag:
            summary = (
                "No strong indications of overfitting were detected. "
                "The feature-to-sample ratio is reasonable and no highly correlated "
                "feature pairs were found."
            )
        else:
            issues = []
            if ratio_flag:
                issues.append(
                    f"high feature-to-sample ratio ({feature_ratio:.2f})"
                )
            if correlation_flag:
                issues.append(
                    f"{high_corr_pairs} highly correlated feature pairs"
                )

            summary = (
                "Potential overfitting risk detected due to "
                + " and ".join(issues)
                + ". This may cause the model to memorize the training data "
                 "rather than generalize well to unseen data."
            )

        return {
            "n_samples": n_samples,
            "n_features": n_features,
            "feature_to_sample_ratio": round(feature_ratio, 4),
            "high_correlation_pairs": high_corr_pairs,
            "overfitting_risk": bool(ratio_flag or correlation_flag),
            "summary": summary
        }

    def data_leakage_check(self):
        """
        Searches for leakage features:
        - Column names suggesting target/label.
        - Extremely high correlation with target-like columns.
        """
        if self.data is None:
            raise ValueError("Data not loaded.")

        suspicious_columns = [
            col for col in self.data.columns
            if 'target' in col.lower() or 'label' in col.lower()
        ]

        correlations = self.data.corr(numeric_only=True)
        leakage_features = []

        if suspicious_columns:
            target = suspicious_columns[0]
            if target in correlations:
                for col, value in correlations[target].items():
                    if abs(value) > 0.95 and col != target:
                        leakage_features.append(col)

        #  Summary logic
        if not suspicious_columns:
            summary = (
                "No obvious data leakage risks were detected. "
                "No columns appear to directly encode the target variable."
            )
        elif suspicious_columns and not leakage_features:
            summary = (
                f"Potential target-like column(s) detected: {suspicious_columns}. "
                "However, no other features show extremely high correlation with them."
            )
        else:
            summary = (
                f"High risk of data leakage detected. "
                f"Target-like columns found: {suspicious_columns}. "
                f"Highly correlated features: {leakage_features}. "
                "These features may leak target information into the model."
            )   

        return {
            "suspected_target_columns": suspicious_columns,
            "high_target_correlations": leakage_features,
            "leakage_risk": bool(suspicious_columns or leakage_features),
            "summary": summary
        }


    def miss_values_check(self):
        """
        Analyze missing values:
        - Percentage missing per column.
        - Columns with extremely high missing rates.
        """
        if self.data is None:
            raise ValueError("Data not loaded.")


        missing_percent = self.data.isnull().mean() * 100
        high_missing = missing_percent[missing_percent > 50].index.tolist()


        summary = (
            f"{len(high_missing)} columns have more than 50% missing values."
            if high_missing else
            "No columns with critically high missing values detected."
        )

        return {
        "missing_percentages": missing_percent.to_dict(),
        "high_missing_columns": high_missing,
        "summary":summary
        }


    def out_impact_check(self):
        """
        Detect outliers and estimate their potential impact:
        - Z-score outlier detection.
        - Count of outliers per column.
        """

        if self.data is None:
            raise ValueError("Data not loaded.")

        numeric_data = self.data.select_dtypes(include=[np.number])

        if numeric_data.empty:
            return {
                "outliers_per_column": {},
                "total_outliers": 0,
                "summary": "No numeric columns available for outlier detection."
            }

        z_scores = np.abs(zscore(numeric_data, nan_policy='omit'))
        outlier_mask = z_scores > 3

        outlier_counts = pd.Series(
            outlier_mask.sum(axis=0),
            index=numeric_data.columns
        )

        total_outliers = int(outlier_counts.sum())
        affected_columns = outlier_counts[outlier_counts > 0].index.tolist()

        #  Summary logic
        if total_outliers == 0:
            summary = (
                "No significant outliers were detected. "
                "All numeric features appear to be within normal statistical ranges."
            )
        else:
            summary = (
                f"A total of {total_outliers} potential outliers were detected across "
                f"{len(affected_columns)} numeric feature(s). "
                f"Columns affected: {affected_columns}. "
                "These extreme values may disproportionately influence model training "
                "and should be reviewed or treated."
            )

        return {
            "outliers_per_column": outlier_counts.to_dict(),
            "total_outliers": total_outliers,
            "affected_columns": affected_columns,
            "summary": summary
        }

