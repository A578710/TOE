import streamlit as st  # Імпорт Streamlit
import numpy as np
import matplotlib.pyplot as plt

# Функція для обчислення комплексного вигляду сигналу
def signal_to_complex(amplitude, phase_deg):
    rms_value = amplitude / np.sqrt(2)  # Перехід до діючого значення
    phase_rad = np.radians(phase_deg)  # Перетворення фази в радіани
    complex_form = rms_value * np.exp(1j * phase_rad)  # Показова форма
    return complex_form

# Функція для побудови векторної діаграми з ергономічною інформацією
def plot_ergonomic_vector_diagram(signals, sum_signal):
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    
    # Візуалізація окремих сигналів
    for i, signal in enumerate(signals, 1):
        # Побудова вектора
        plt.quiver(0, 0, signal.real, signal.imag, angles='xy', scale_units='xy', scale=1,
                   color=f'C{i}', label=f"Сигнал {i}")
        
        # Додавання текстової інформації для кожного сигналу
        plt.text(signal.real, signal.imag,
                 f" |{np.abs(signal):.2f}| ∠ {np.degrees(np.angle(signal)):.2f}°",
                 fontsize=10, color=f'C{i}', ha='left', va='bottom')

        # Позначення проекцій на осі
        plt.plot([signal.real, signal.real], [0, signal.imag], linestyle='dotted', color=f'C{i}')
        plt.plot([0, signal.real], [signal.imag, signal.imag], linestyle='dotted', color=f'C{i}')

    # Візуалізація суми
    plt.quiver(0, 0, sum_signal.real, sum_signal.imag, angles='xy', scale_units='xy', scale=1,
               color='red', label="Сума", linewidth=2)
    
    # Додавання текстової інформації для суми
    plt.text(sum_signal.real, sum_signal.imag,
             f" |{np.abs(sum_signal):.2f}| ∠ {np.degrees(np.angle(sum_signal)):.2f}°",
             fontsize=12, color='red', ha='left', va='bottom')

    # Позначення проекцій на осі для суми
    plt.plot([sum_signal.real, sum_signal.real], [0, sum_signal.imag], linestyle='dotted', color='red')
    plt.plot([0, sum_signal.real], [sum_signal.imag, sum_signal.imag], linestyle='dotted', color='red')

    # Налаштування координатної сітки
    max_limit = max(max(abs(sig.real), abs(sig.imag)) for sig in signals + [sum_signal]) * 1.2
    plt.xlim(-max_limit, max_limit)
    plt.ylim(-max_limit, max_limit)
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.grid(True, linestyle='--', alpha=0.5)

    # Підписи осей
    plt.xlabel("Реальна частина (Re)", fontsize=12)
    plt.ylabel("Уявна частина (Im)", fontsize=12)
    
    # Легенда та заголовок
    plt.title("Ергономічна векторна діаграма синусоїдальних величин", fontsize=14)
    plt.legend(fontsize=10, loc='upper left')
    
    st.pyplot(plt)

# Основний додаток
st.title("Симулятор: Векторна діаграма для синусоїдальних сигналів")

# Вибір кількості сигналів
st.sidebar.header("Налаштування")
num_signals = st.sidebar.slider("Кількість сигналів", min_value=1, max_value=5, value=2)

# Введення параметрів сигналів
signals = []
st.header("Параметри сигналів")
for i in range(num_signals):
    st.subheader(f"Сигнал {i + 1}")
    amplitude = st.number_input(f"Амплітудне значення сигналу {i + 1} (A)", value=10.0, key=f"amp_{i}")
    phase_deg = st.number_input(f"Фаза сигналу {i + 1} (градуси)", value=30.0, key=f"phase_{i}")
    signals.append(signal_to_complex(amplitude, phase_deg))

# Перевірка наявності сигналів перед обчисленнями
if signals:
    # Розрахунок суми сигналів
    sum_signals = sum(signals)
    
    # Побудова векторної діаграми
    st.subheader("Ергономічна векторна діаграма")
    plot_ergonomic_vector_diagram(signals, sum_signals)
else:
    st.warning("Додайте хоча б один сигнал для побудови діаграми.")
