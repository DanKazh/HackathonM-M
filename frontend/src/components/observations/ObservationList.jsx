import React, { useState } from 'react';
import styles from './ObservationList.module.css';
import { MIN_OBSERVATIONS } from '../../utils/constants';
import { formatDateTime, formatNumber } from '../../utils/formatters';

const ObservationList = ({ 
  observations, 
  onUpdateObservation, 
  onDeleteObservation, 
  onClearObservations, 
  onCalculate 
}) => {
  const [deletingId, setDeletingId] = useState(null);
  const [rearrangingIds, setRearrangingIds] = useState([]);

  const canCalculate = observations.length >= MIN_OBSERVATIONS;

  const handleDelete = (id) => {
    setDeletingId(id);
    
    // Находим индекс удаляемой строки
    const deleteIndex = observations.findIndex(obs => obs.id === id);
    
    // Определяем какие строки нужно анимировать (все что ниже удаляемой)
    const rowsToRearrange = observations
      .slice(deleteIndex + 1)
      .map(obs => obs.id);
    
    setRearrangingIds(rowsToRearrange);
    
    // Анимация смахивания
    setTimeout(() => {
      onDeleteObservation(id);
      setDeletingId(null);
      
      // Убираем класс перестроения после завершения анимации
      setTimeout(() => {
        setRearrangingIds([]);
      }, 600);
    }, 400);
  };

  const handleCalculateOrbit = () => {
    if (canCalculate) {
      onCalculate(observations);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.observationList}>
        <h2 className={styles.title}>Список наблюдений ({observations.length})</h2>
        
        {observations.length === 0 ? (
          <div className={styles.emptyState}>
            <p>Наблюдения отсутствуют</p>
            <p className={styles.hint}>Добавьте минимум {MIN_OBSERVATIONS} наблюдений для расчета орбиты</p>
          </div>
        ) : (
          <>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>№</th>
                  <th>Дата/Время (UTC)</th>
                  <th>RA (°)</th>
                  <th>Dec (°)</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                {observations.map((obs, index) => {
                  const ra = parseFloat(obs.ra);
                  const dec = parseFloat(obs.dec);
                  
                  return (
                    <tr 
                      key={obs.id} 
                      className={`${styles.row} ${
                        deletingId === obs.id ? styles.deleting : ''
                      } ${
                        rearrangingIds.includes(obs.id) ? styles.rearranging : ''
                      }`}
                    >
                      <td>
                        <span className={styles.cellContent}>
                          {index + 1}
                          {deletingId === obs.id && <div className={styles.strikeThrough}></div>}
                        </span>
                      </td>
                      <td>
                        <span className={styles.cellContent}>
                          {formatDateTime(obs.date)}
                          {deletingId === obs.id && <div className={styles.strikeThrough}></div>}
                        </span>
                      </td>
                      <td>
                        <span className={styles.cellContent}>
                          {isNaN(ra) ? obs.ra : formatNumber(ra)}
                          {deletingId === obs.id && <div className={styles.strikeThrough}></div>}
                        </span>
                      </td>
                      <td>
                        <span className={styles.cellContent}>
                          {isNaN(dec) ? obs.dec : formatNumber(dec)}
                          {deletingId === obs.id && <div className={styles.strikeThrough}></div>}
                        </span>
                      </td>
                      <td>
                        <button 
                          className={styles.deleteBtn}
                          onClick={() => handleDelete(obs.id)}
                          disabled={deletingId}
                        >
                          Удалить
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            <div className={styles.footer}>
              <button 
                className={styles.calculateBtn} 
                onClick={handleCalculateOrbit}
                disabled={!canCalculate}
              >
                {canCalculate 
                  ? 'Рассчитать орбиту' 
                  : `Нужно ещё ${MIN_OBSERVATIONS - observations.length} наблюдений`}
              </button>
              <button 
                className={styles.clearBtn}
                onClick={onClearObservations}
                disabled={observations.length === 0}
              >
                Очистить все
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ObservationList;