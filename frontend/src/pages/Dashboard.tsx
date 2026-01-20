import React, { useState, useEffect } from 'react'
import { FiPlus, FiEdit2, FiTrash2, FiChevronRight } from 'react-icons/fi'
import api from '../services/api'
import '../styles/dashboard.css'

interface Domain {
  name: string
  records?: any[]
}

const Dashboard: React.FC = () => {
  const [domains, setDomains] = useState<Domain[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null)

  useEffect(() => {
    fetchDomains()
  }, [])

  const fetchDomains = async () => {
    try {
      setLoading(true)
      const response = await api.getDomains()
      setDomains(response.data)
    } catch (err: any) {
      setError('Failed to fetch domains')
    } finally {
      setLoading(false)
    }
  }

  const handleSelectDomain = async (domain: Domain) => {
    try {
      const response = await api.getDomain(domain.name)
      setSelectedDomain(response.data)
    } catch (err) {
      setError('Failed to fetch domain details')
    }
  }

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>DNS Management</h1>
        <button className="btn btn-primary">
          <FiPlus /> Add Domain
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="dashboard-grid">
        <div className="domains-section">
          <h2>Your Domains</h2>
          <div className="domains-list">
            {domains.length === 0 ? (
              <p className="empty-state">No domains found</p>
            ) : (
              domains.map((domain) => (
                <div
                  key={domain.name}
                  className={`domain-item ${selectedDomain?.name === domain.name ? 'active' : ''}`}
                  onClick={() => handleSelectDomain(domain)}
                >
                  <div className="domain-info">
                    <h3>{domain.name}</h3>
                    <p>0 DNS records</p>
                  </div>
                  <FiChevronRight />
                </div>
              ))
            )}
          </div>
        </div>

        <div className="records-section">
          {selectedDomain ? (
            <>
              <div className="records-header">
                <h2>{selectedDomain.name} Records</h2>
                <button className="btn btn-primary">
                  <FiPlus /> Add Record
                </button>
              </div>

              <div className="records-table">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Type</th>
                      <th>Content</th>
                      <th>TTL</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedDomain.records && selectedDomain.records.length > 0 ? (
                      selectedDomain.records.map((record) => (
                        <tr key={record.id}>
                          <td>{record.name}</td>
                          <td><span className="badge badge-primary">{record.type}</span></td>
                          <td>{record.content}</td>
                          <td>{record.ttl}</td>
                          <td className="actions">
                            <button className="btn-icon">
                              <FiEdit2 />
                            </button>
                            <button className="btn-icon danger">
                              <FiTrash2 />
                            </button>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={5} className="empty-state">No DNS records</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <div className="empty-state-large">
              <p>Select a domain to view DNS records</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
