import { Eye, Trash2 } from 'lucide-react'
import { formatDate, getStatusLabel } from '../utils/formatters.js'

export default function CvTable({ items, onOpenDetails, onDelete }) {
  return (
    <div className="table-card">
      <table className="cv-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nazwa pliku</th>
            <th>Data przesłania</th>
            <th>Status</th>
            <th>Akcje</th>
          </tr>
        </thead>

        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td className="file-name">{item.filename}</td>
              <td>{formatDate(item.upload_date)}</td>
              <td>
                <span className={`status-badge status-${item.status || 'unknown'}`}>
                  {getStatusLabel(item.status)}
                </span>
              </td>
              <td>
                <div className="row-actions">
                  <button className="icon-button" type="button" onClick={() => onOpenDetails(item.id)} title="Szczegóły">
                    <Eye size={18} />
                  </button>

                  <button className="icon-button danger" type="button" onClick={() => onDelete(item.id)} title="Usuń">
                    <Trash2 size={18} />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}