import React from 'react';
import { useObservations } from '../../hooks/useObservations';
import Button from '../common/Button';
import { MIN_OBSERVATIONS } from '../../utils/constants';
import { formatDateTime, formatNumber } from '../../utils/formatters';
import './ObservationTable.css';

function ObservationTable({ onCalculate }) {
  const { observations, removeObservation, clearObservations } = useObservations();

  const canCalculate = observations.length >= MIN_OBSERVATIONS;

  return (
    <div className="observation-table-container">
      <h3>Список наблюдений ({observations.length})</h3>
      
      {observations.length === 0 ? (
        <div className="empty-state">
          <p>📡 Наблюдения отсутствуют</p>
          <p className="hint">Добавьте минимум {MIN_OBSERVATIONS} наблюдений для расчета орбиты</p>
        </div>
      ) : (
        <>
          <div className="table-wrapper">
            <table className="observation-table">
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
                {observations.map((obs, index) => (
                  <tr key={obs.id}>
                    <td>{index + 1}</td>
                    <td>{formatDateTime(obs.date)}</td>
                    <td>{formatNumber(obs.ra)}</td>
                    <td>{formatNumber(obs.dec)}</td>
                    <td>
                      <Button
                        variant="danger"
                        className="btn-small"
                        onClick={() => removeObservation(obs.id)}
                      >
                        Удалить
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="button-group">
            <Button
              variant="success"
              onClick={onCalculate}
              disabled={!canCalculate}
            >
              {canCalculate 
                ? 'Рассчитать орбиту' 
                : `Нужно ещё ${MIN_OBSERVATIONS - observations.length} наблюдений`}
            </Button>
            <Button variant="secondary" onClick={clearObservations}>
              Очистить все
            </Button>
          </div>
        </>
      )}
    </div>
  );
}

export default ObservationTable;
