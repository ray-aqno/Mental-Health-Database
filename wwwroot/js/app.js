// =====================================================
// Mental Health Database - Main Application Script
// =====================================================

class MentalHealthApp {
    constructor() {
        this.map = null;
        this.markers = {};
        this.colleges = [];
        this.filteredColleges = [];
        this.currentFilter = 'all';
        this.searchQuery = '';
        this.deviceMode = 'desktop';
        this.resizeTimer = null;
        this.init();
    }

    init() {
        this.detectDeviceMode();
        window.addEventListener('resize', () => this.handleResize());
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.initializeMap();
                this.setupEventListeners();
                this.loadColleges();
            });
        } else {
            this.initializeMap();
            this.setupEventListeners();
            this.loadColleges();
        }
    }

    initializeMap() {
        try {
            if (typeof L === 'undefined') {
                throw new Error('Leaflet library is not loaded.');
            }

            this.map = L.map('map').setView([39.8283, -98.5795], 5);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19,
                minZoom: 4
            }).addTo(this.map);

            console.log('✔ Map initialized successfully');
        } catch (error) {
            console.error('✖ Map initialization failed:', error);
            this.showError('Failed to initialize map: ' + error.message);
        }
    }

    setupEventListeners() {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchQuery = e.target.value.toLowerCase();
                this.filterColleges();
            });
        }

        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });

        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadColleges();
            });
        }

        const sheetClear = document.getElementById('sheet-clear');
        if (sheetClear) {
            sheetClear.addEventListener('click', () => {
                this.clearFilters();
            });
        }
    }

    handleResize() {
        clearTimeout(this.resizeTimer);
        this.resizeTimer = setTimeout(() => this.detectDeviceMode(), 120);
    }

    detectDeviceMode() {
        const isMobile = typeof window.matchMedia === 'function'
            ? window.matchMedia('(max-width: 768px)').matches
            : window.innerWidth <= 768;
        const mode = isMobile ? 'mobile' : 'desktop';
        if (mode !== this.deviceMode) {
            this.deviceMode = mode;
            this.applyDeviceMode();
        }
        const shell = document.getElementById('app-shell');
        if (shell) {
            shell.dataset.deviceMode = mode;
        }
    }

    applyDeviceMode() {
        const sheetTitle = document.querySelector('.sheet-header h3');
        if (sheetTitle) {
            sheetTitle.textContent = this.deviceMode === 'mobile'
                ? 'Tap to filter Hope Squad partners'
                : 'Filter campuses';
        }
    }

    async loadColleges() {
        this.showLoading(true);
        try {
            const response = await fetch('/api/colleges');
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.message || `HTTP error! Status: ${response.status}`;
                throw new Error(errorMessage);
            }

            this.colleges = await response.json();
            console.log(`✔ Loaded ${this.colleges.length} colleges`);

            if (this.colleges.length === 0) {
                this.showInfo('No colleges found in the database. Please add some colleges first.');
            }

            this.filteredColleges = [...this.colleges];
            this.renderColleges();
            this.updateStats();
            this.setMapStatus('Data synchronized');
            this.showLoading(false);
        } catch (error) {
            console.error('✖ Failed to load colleges:', error);
            this.showError('Failed to load college data: ' + error.message + '. The database might not be initialized yet.');
            this.showLoading(false);
        }
    }

    renderColleges() {
        Object.values(this.markers).forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.markers = {};

        const collegeList = document.getElementById('college-list');
        if (collegeList) {
            collegeList.innerHTML = '';
        }

        if (this.filteredColleges.length === 0) {
            this.showInfo('No colleges match your search criteria.');
            this.renderResourceCards();
            this.renderMapMetadata();
            return;
        }

        this.filteredColleges.forEach(college => {
            this.addCollegeMarker(college);
            this.addCollegeToSidebar(college);
        });

        if (this.filteredColleges.length > 0) {
            const bounds = L.latLngBounds(
                this.filteredColleges.map(c => [c.latitude, c.longitude])
            );
            this.map.fitBounds(bounds, { 
                padding: [50, 50],
                maxZoom: 12
            });
        }

        const countElement = document.getElementById('college-count');
        if (countElement) {
            countElement.textContent = this.filteredColleges.length;
        }

        this.renderResourceCards();
        this.updateActiveFilterBadge();
        this.renderMapMetadata();
    }

    renderResourceCards() {
        const container = document.getElementById('resource-cards');
        if (!container) return;

        container.innerHTML = '';

        if (this.filteredColleges.length === 0) {
            container.innerHTML = `
                <div class="resource-card empty">
                    <h4>No results</h4>
                    <p>Try a broader search or clear the filters.</p>
                </div>
            `;
            return;
        }

        this.filteredColleges.slice(0, 4).forEach(college => {
            const card = document.createElement('article');
            card.className = 'resource-card';
            card.dataset.collegeId = college.id;

            const resourceCount = college.resources ? college.resources.length : 0;
            const highlightResource = college.resources && college.resources.length > 0
                ? college.resources[0].serviceName
                : 'Resources pending';

            card.innerHTML = `
                <div class="resource-card-top">
                    <h4>${college.name}</h4>
                    <p class="resource-card-meta">${college.location || 'Location TBD'}</p>
                </div>
                <p>${highlightResource}</p>
                <p>${resourceCount} resource${resourceCount !== 1 ? 's' : ''} available</p>
                <div class="resource-card-cta">
                    <span>Tap to focus</span>
                    <a href="${college.website}" target="_blank" rel="noopener" class="resource-card-link">Visit site →</a>
                </div>
            `;

            card.addEventListener('click', () => {
                this.zoomToCollege(college);
                this.highlightCollege(college.id);
            });

            container.appendChild(card);
        });
    }

    renderMapMetadata() {
        const totalCampuses = this.filteredColleges.length;
        const totalResources = this.filteredColleges.reduce((sum, college) => {
            return sum + (college.resources ? college.resources.length : 0);
        }, 0);

        const states = new Set(
            this.filteredColleges.map(c => {
                const parts = c.location ? c.location.split(',') : [];
                return parts.length ? parts[parts.length - 1].trim() : 'Unknown';
            })
        );

        const metaElements = {
            'meta-colleges': totalCampuses,
            'meta-resources': totalResources,
            'meta-states': states.size
        };

        Object.entries(metaElements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });

        const list = document.getElementById('metadata-list');
        if (!list) return;

        list.innerHTML = '';
        if (totalCampuses === 0) {
            list.innerHTML = '<li>No campuses in view. Adjust filters to see Hope Squad partners.</li>';
            return;
        }

        this.filteredColleges.slice(0, 3).forEach((college, index) => {
            const item = document.createElement('li');
            const resourceCount = college.resources ? college.resources.length : 0;
            item.innerHTML = `
                <strong>${index + 1}. ${college.name}</strong>
                <span>${college.location || 'Midwest region'} • ${resourceCount} resource${resourceCount !== 1 ? 's' : ''}</span>
            `;
            list.appendChild(item);
        });
    }

    addCollegeMarker(college) {
        const marker = L.marker([college.latitude, college.longitude], {
            title: college.name
        })
        .addTo(this.map)
        .bindPopup(() => this.createPopupContent(college), {
            maxWidth: 450,
            maxHeight: 500,
            className: 'custom-popup'
        });

        marker.on('click', () => {
            this.highlightCollege(college.id);
        });

        this.markers[college.id] = marker;
    }

    addCollegeToSidebar(college) {
        const collegeList = document.getElementById('college-list');
        if (!collegeList) return;

        const listItem = document.createElement('li');
        listItem.className = 'college-item';
        listItem.dataset.collegeId = college.id;

        const resourceCount = college.resources ? college.resources.length : 0;

        listItem.innerHTML = `
            <div class="college-item-name">${college.name}</div>
            <div class="college-item-location">📍 ${college.location}</div>
            <div class="college-item-resources">🔥 ${resourceCount} resource${resourceCount !== 1 ? 's' : ''}</div>
        `;

        listItem.addEventListener('click', () => {
            this.zoomToCollege(college);
            this.highlightCollege(college.id);
        });

        collegeList.appendChild(listItem);
    }

    createPopupContent(college) {
        const container = document.createElement('div');
        container.className = 'resource-popup';

        const header = document.createElement('div');
        header.className = 'popup-header';
        header.innerHTML = `
            <h3>${college.name}</h3>
            <div class="popup-location">📍 ${college.location}</div>
            <div class="popup-website">
                <a href="${college.website}" target="_blank" rel="noopener noreferrer">
                    🌐 Visit Website →
                </a>
            </div>
        `;
        container.appendChild(header);

        if (college.resources && college.resources.length > 0) {
            const resourcesSection = document.createElement('div');
            resourcesSection.className = 'resources-section';

            const resourcesHeader = document.createElement('div');
            resourcesHeader.className = 'resources-header';
            resourcesHeader.innerHTML = '🧭 Mental Health Resources';
            resourcesSection.appendChild(resourcesHeader);

            college.resources.forEach(resource => {
                const resourceDiv = this.createResourceElement(resource);
                resourcesSection.appendChild(resourceDiv);
            });

            container.appendChild(resourcesSection);
        } else {
            const noResources = document.createElement('p');
            noResources.className = 'text-center mt-2';
            noResources.style.color = 'var(--text-light)';
            noResources.textContent = 'No resources available yet.';
            container.appendChild(noResources);
        }

        return container;
    }

    createResourceElement(resource) {
        const div = document.createElement('div');
        div.className = 'resource-item';

        const name = document.createElement('div');
        name.className = 'resource-name';
        name.textContent = resource.serviceName;
        div.appendChild(name);

        if (resource.description) {
            const desc = document.createElement('div');
            desc.className = 'resource-description';
            desc.textContent = resource.description;
            div.appendChild(desc);
        }

        const details = [];

        if (resource.department) {
            details.push({ icon: '🏫', label: 'Department', value: resource.department });
        }

        if (resource.contactEmail) {
            details.push({ 
                icon: '✉️',
                label: 'Email',
                value: `<a href="mailto:${resource.contactEmail}">${resource.contactEmail}</a>`
            });
        }

        if (resource.contactPhone) {
            details.push({ 
                icon: '📞',
                label: 'Phone',
                value: `<a href="tel:${resource.contactPhone}">${resource.contactPhone}</a>`
            });
        }

        if (resource.officeHours) {
            details.push({ icon: '⏰', label: 'Hours', value: resource.officeHours });
        }

        if (resource.location) {
            details.push({ icon: '📍', label: 'Location', value: resource.location });
        }

        if (resource.contactWebsite) {
            details.push({ 
                icon: '🌐',
                label: 'Website',
                value: `<a href="${resource.contactWebsite}" target="_blank" rel="noopener noreferrer">Learn More</a>`
            });
        }

        details.forEach(detail => {
            const detailDiv = document.createElement('div');
            detailDiv.className = 'resource-detail';
            detailDiv.innerHTML = `
                <span class="resource-detail-icon">${detail.icon}</span>
                <span class="resource-detail-label">${detail.label}:</span>
                <span class="resource-detail-value">${detail.value}</span>
            `;
            div.appendChild(detailDiv);
        });

        if (resource.freshmanNotes) {
            const freshmanDiv = document.createElement('div');
            freshmanDiv.className = 'freshman-notes';
            freshmanDiv.innerHTML = `
                <div class="freshman-notes-label">
                    🎓 Important for Freshmen
                </div>
                <div class="freshman-notes-text">
                    ${resource.freshmanNotes}
                </div>
            `;
            div.appendChild(freshmanDiv);
        }

        return div;
    }

    filterColleges() {
        this.filteredColleges = this.colleges.filter(college => {
            const matchesSearch = this.searchQuery === '' || 
                college.name.toLowerCase().includes(this.searchQuery) ||
                college.location.toLowerCase().includes(this.searchQuery);

            let matchesFilter = true;
            if (this.currentFilter !== 'all') {
                matchesFilter = college.location.toLowerCase().includes(this.currentFilter.toLowerCase());
            }

            return matchesSearch && matchesFilter;
        });

        this.renderColleges();
        this.updateStats();
        this.setMapStatus('Filters updated');
    }

    setFilter(filter) {
        this.currentFilter = filter;

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === filter) {
                btn.classList.add('active');
            }
        });

        this.filterColleges();
    }

    clearFilters() {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = '';
        }
        this.searchQuery = '';
        this.setFilter('all');
    }

    zoomToCollege(college) {
        this.map.setView([college.latitude, college.longitude], 13);
        const marker = this.markers[college.id];
        if (marker) {
            marker.openPopup();
        }
    }

    highlightCollege(collegeId) {
        document.querySelectorAll('.college-item').forEach(item => {
            item.classList.remove('active');
            if (parseInt(item.dataset.collegeId) === collegeId) {
                item.classList.add('active');
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });

        document.querySelectorAll('.resource-card').forEach(card => {
            card.classList.remove('active');
            if (parseInt(card.dataset.collegeId) === collegeId) {
                card.classList.add('active');
            }
        });
    }

    updateStats() {
        const totalColleges = this.filteredColleges.length;
        const totalResources = this.filteredColleges.reduce((sum, college) => {
            return sum + (college.resources ? college.resources.length : 0);
        }, 0);

        const states = new Set(
            this.filteredColleges.map(c => {
                const parts = c.location.split(',');
                return parts[parts.length - 1].trim();
            })
        );

        const statsElements = {
            'stat-colleges': totalColleges,
            'stat-resources': totalResources,
            'stat-states': states.size
        };

        Object.entries(statsElements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    setMapStatus(status) {
        const paceElement = document.getElementById('map-pace');
        if (paceElement) {
            paceElement.textContent = status;
        }
    }

    updateActiveFilterBadge() {
        const labelElement = document.getElementById('active-filter');
        if (labelElement) {
            labelElement.textContent = this.currentFilter === 'all' ? 'All States' : this.currentFilter;
        }
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        const mapElement = document.getElementById('map');
        if (loadingElement) {
            loadingElement.style.display = show ? 'block' : 'none';
        }
        if (mapElement) {
            mapElement.style.opacity = show ? '0.5' : '1';
        }
    }

    showError(message) {
        this.showAlert('error', message);
    }

    showInfo(message) {
        this.showAlert('info', message);
    }

    showSuccess(message) {
        this.showAlert('success', message);
    }

    showAlert(type, message) {
        const container = document.getElementById('alert-container');
        if (!container) return;

        const alert = document.createElement('div');
        alert.className = `alert ${type} fade-in`;
        const icons = {
            error: '✖',
            success: '✔',
            info: 'ℹ️'
        };

        alert.innerHTML = `
            <span class="alert-icon">${icons[type] || 'ℹ️'}</span>
            <div class="alert-content">${message}</div>
            <button class="alert-close" onclick="this.parentElement.remove()">×</button>
        `;

        container.appendChild(alert);

        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 5000);
    }
}

const app = new MentalHealthApp();
window.app = app;
