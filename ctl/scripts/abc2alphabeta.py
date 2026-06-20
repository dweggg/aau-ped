import math

def abc_to_alphabeta(a, b, c):
    alpha = (2/3) * (a - 0.5*b - 0.5*c)
    beta  = (2/3) * ((math.sqrt(3)/2) * (b - c))
    zero  = (a + b + c) / 3
    return alpha, beta, zero


def alphabeta_to_abc(alpha, beta, zero):
    a = alpha + zero
    b = -0.5 * alpha + (math.sqrt(3)/2) * beta + zero
    c = -0.5 * alpha - (math.sqrt(3)/2) * beta + zero
    return a, b, c

def alphabeta_to_dq(alpha, beta, theta):
    """
    Park transform (stationary αβ -> rotating dq)

    theta: electrical angle [rad]

    Returns:
        d, q
    """
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    d = alpha * cos_t + beta * sin_t
    q = -alpha * sin_t + beta * cos_t

    return d, q


def dq_to_alphabeta(d, q, theta):
    """
    Inverse Park transform (rotating dq -> stationary αβ)

    theta: electrical angle [rad]

    Returns:
        alpha, beta
    """
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    alpha = d * cos_t - q * sin_t
    beta  = d * sin_t + q * cos_t

    return alpha, beta

def vector_mag_angle(*, a=None, b=None, c=None, alpha=None, beta=None):
    """
    Return magnitude and angle of the space vector.

    Use either:
      - a, b, c
      - alpha, beta

    Returns:
      magnitude, angle_rad, angle_deg
    """
    if alpha is None or beta is None:
        if a is None or b is None or c is None:
            raise ValueError("Provide either (a, b, c) or (alpha, beta).")
        alpha, beta, _ = abc_to_alphabeta(a, b, c)

    magnitude = math.hypot(alpha, beta)
    angle_rad = math.atan2(beta, alpha)
    angle_deg = math.degrees(angle_rad)

    return magnitude, angle_rad, angle_deg


if __name__ == "__main__":
    a, b, c = 10.0, -5.0, -5.0

    alpha, beta, zero = abc_to_alphabeta(a, b, c)
    print(f"alpha = {alpha:.4f}, beta = {beta:.4f}, zero = {zero:.4f}")

    mag, ang_rad, ang_deg = vector_mag_angle(a=a, b=b, c=c)
    print(f"magnitude = {mag:.4f}, angle = {ang_rad:.4f} rad, {ang_deg:.2f} deg")

    alpha, beta, zero = 0.0, 10.0, 0.0
    a, b, c = alphabeta_to_abc(alpha, beta, zero)
    print(f"aaaa = {a:.4f}, b = {b:.4f}, c = {c:.4f}")

    mag, ang_rad, ang_deg = vector_mag_angle(a=a, b=b, c=c)
    print(f"magnitude = {mag:.4f}, angle = {ang_rad:.4f} rad, {ang_deg:.2f} deg")

    theta = math.radians(33.69)
    d, q = alphabeta_to_dq(alpha, beta, theta)
    print(f"d = {d:.4f}, q = {q:.4f}")

    alpha, beta = dq_to_alphabeta(0, 10, 0)
    print(f"alpha = {alpha:.4f}, beta = {beta:.4f}")
