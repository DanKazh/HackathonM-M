export function formatDateTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

export function formatDate(dateString) {
  const date = new Date(dateString);
  const readyDate = date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  return readyDate;
}

export function formatDateFull(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

export const formatNumber = (value, options = {}) => {
  const {
    precision = 4,
    compact = false,
    notation = 'auto'
  } = options;

  // Проверка на нечисловые значения
  if (value === null || value === undefined || isNaN(value)) {
    return '-';
  }

  // Для целых чисел
  if (Number.isInteger(value)) {
    return value.toString();
  }

  // Для очень маленьких чисел (близких к нулю)
  if (Math.abs(value) < 1e-10 && value !== 0) {
    return value.toExponential(precision);
  }

  // Автоматический выбор нотации
  let actualNotation = notation;
  if (notation === 'auto') {
    if (Math.abs(value) >= 1e6 || (Math.abs(value) < 1e-3 && value !== 0)) {
      actualNotation = 'scientific';
    } else {
      actualNotation = 'standard';
    }
  }

  // Научная нотация
  if (actualNotation === 'scientific') {
    return value.toExponential(precision);
  }

  // Компактный формат для больших чисел
  if (compact && Math.abs(value) >= 1000) {
    const formats = [
      { value: 1e9, suffix: ' млрд' },
      { value: 1e6, suffix: ' млн' },
      { value: 1e3, suffix: ' тыс' }
    ];

    const format = formats.find(f => Math.abs(value) >= f.value);
    if (format) {
      const formatted = (value / format.value).toFixed(precision);
      return formatted.replace(/\.?0+$/, '') + format.suffix;
    }
  }

  // Стандартное форматирование
  const fixed = value.toFixed(precision);
  
  // Убираем лишние нули после запятой
  return fixed.replace(/\.?0+$/, '');
};
