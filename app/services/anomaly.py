import numpy as np
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity

def vectorize_behavior(behavior: dict) -> np.ndarray:
    cmds = behavior.get("commands", [])
    cints = behavior.get("command_intervals", [])
    files = behavior.get("file_accessed", [])
    kints = behavior.get("keystroke_intervals", [])

    features = [
        len(cmds),
        float(np.mean(cints)) if cints else 0.0,
        float(np.std(cints))  if cints else 0.0,
        len(files),
        float(np.mean(kints)) if kints else 0.0,
        float(np.std(kints))  if kints else 0.0,
    ]
    return np.array(features)

def compute_mahalanobis(curr, hist_mat):
    cov     = np.cov(hist_mat, rowvar=False)
    inv_cov = np.linalg.pinv(cov)
    mean_v  = np.mean(hist_mat, axis=0)
    return float(distance.mahalanobis(curr, mean_v, inv_cov))

def compute_cosine(curr, hist_mat):
    hist_mean = np.mean(hist_mat, axis=0).reshape(1, -1)
    curr_vec  = curr.reshape(1, -1)
    return float(cosine_similarity(curr_vec, hist_mean)[0][0])

def compute_anomaly_score(curr_vec, hist_vecs):
    m_dist = compute_mahalanobis(curr_vec, hist_vecs)
    score_maha = m_dist / (m_dist + 1)
    cos_dev = 1 - compute_cosine(curr_vec, hist_vecs)
    # Weighted average: heavier on Mahalanobis
    final_score = 0.7 * score_maha + 0.3 * cos_dev
    return final_score, {"mahalanobis": score_maha, "cosine_dev": cos_dev}
