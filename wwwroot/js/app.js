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
        this.mapStatus = 'Search ready';
        this.isPanelCondensed = true;
        this.panelToggleBtn = null;
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

        const panelToggle = document.getElementById('toggle-panel-view');
        if (panelToggle) {
            this.panelToggleBtn = panelToggle;
            panelToggle.addEventListener('click', () => this.togglePanelLayout());
        }

        this.applyPanelLayout();
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
                ? 'Tap to filter nearby campuses'
                : 'Filter campuses';
        }
    }

    togglePanelLayout() {
        this.isPanelCondensed = !this.isPanelCondensed;
        this.applyPanelLayout();
    }

    applyPanelLayout() {
        const panel = document.querySelector('.resource-panel');
        if (!panel) return;
        panel.classList.toggle('condensed', this.isPanelCondensed);
        if (this.panelToggleBtn) {
            this.panelToggleBtn.textContent = this.isPanelCondensed ? 'Expand list' : 'Condense view';
            this.panelToggleBtn.setAttribute('aria-pressed', String(!this.isPanelCondensed));
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

        const visibleColleges = this.deviceMode === 'mobile'
            ? this.filteredColleges
            : this.filteredColleges.slice(0, 4);

        visibleColleges.forEach(college => {
            const card = document.createElement('article');
            card.className = 'resource-card';
            card.dataset.collegeId = college.id;

            const resourceCount = college.resources ? college.resources.length : 0;
            const highlightResource = college.resources && college.resources.length > 0
                ? college.resources[0].serviceName
                : 'Resources pending';

            const websiteUrl = college.website || '#';

            card.innerHTML = `
                <div class="resource-card-top">
                    <h4>${college.name || 'Campus partner'}</h4>
                    <p class="resource-card-meta">${college.location || 'Location TBD'}</p>
                </div>
                <p class="resource-card-highlight">${highlightResource}</p>
                <p class="resource-card-count">${resourceCount} resource${resourceCount !== 1 ? 's' : ''} available</p>
                <div class="resource-card-cta">
                    <span>Tap to focus</span>
                    <a href="${websiteUrl}" target="_blank" rel="noopener" class="resource-card-link">Visit site →</a>
                </div>
            `;

            const detailBlock = document.createElement('div');
            detailBlock.className = 'card-details';
            this.populateCollegeDetails(detailBlock, college);

            const toggleButton = document.createElement('button');
            toggleButton.type = 'button';
            toggleButton.className = 'toggle-details card-toggle';
            toggleButton.textContent = 'More info';
            toggleButton.setAttribute('aria-expanded', 'false');
            toggleButton.addEventListener('click', (event) => {
                event.stopPropagation();
                this.toggleDetails(detailBlock, toggleButton);
            });

            card.appendChild(detailBlock);
            card.appendChild(toggleButton);

            card.addEventListener('click', () => {
                this.zoomToCollege(college);
                this.highlightCollege(college.id);
            });

            container.appendChild(card);
        });

        container.querySelectorAll('.card-details').forEach(details => {
            details.classList.remove('expanded');
        });
        container.classList.toggle('has-scroll', visibleColleges.length > 3);
    }

    renderMapMetadata() {
        const totalCampuses = this.filteredColleges.length;
        const totalResources = this.filteredColleges.reduce((sum, college) => {
            return sum + (college.resources ? college.resources.length : 0);
        }, 0);

        const stateCounts = {};
        this.filteredColleges.forEach(college => {
            const parts = college.location ? college.location.split(',') : [];
            const state = parts.length ? parts[parts.length - 1].trim() : 'Midwest region';
            stateCounts[state] = (stateCounts[state] || 0) + 1;
        });

        const states = new Set(Object.keys(stateCounts));

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

        const topStateEntry = Object.entries(stateCounts)
            .sort((a, b) => b[1] - a[1])[0];
        const topStateLabel = topStateEntry
            ? `${topStateEntry[0]} • ${topStateEntry[1]} campus${topStateEntry[1] !== 1 ? 'es' : ''}`
            : 'Midwest region';

        const featuredCampus = this.filteredColleges[0];
        const featuredCampusText = featuredCampus
            ? `${featuredCampus.name} • ${featuredCampus.location || 'Midwest region'} • ${featuredCampus.resources ? featuredCampus.resources.length : 0} resource${featuredCampus.resources && featuredCampus.resources.length === 1 ? '' : 's'}`
            : 'Campus highlights coming soon';

        const featuredService = featuredCampus && featuredCampus.resources && featuredCampus.resources[0]
            ? featuredCampus.resources[0].serviceName
            : 'Services incoming';

        const formattedFilterLabel = this.formatFilterLabel(this.currentFilter);
        const filterSnapshot = this.currentFilter === 'all'
            ? 'All states in view'
            : `Filtered by ${formattedFilterLabel}`;

        const list = document.getElementById('metadata-list');
        if (!list) return;

        list.innerHTML = '';

        if (totalCampuses === 0) {
            const emptyCard = document.createElement('li');
            emptyCard.className = 'metadata-card';
            emptyCard.innerHTML = `
                <strong>Empty atlas</strong>
                <span>Add colleges or clear filters to populate insights.</span>
            `;
            list.appendChild(emptyCard);
            return;
        }

        const highlights = [
            { label: 'Campus spotlight', value: featuredCampusText },
            { label: 'Most mapped region', value: topStateLabel },
            { label: 'Featured resource', value: featuredService },
            { label: 'Filter snapshot', value: filterSnapshot }
        ];

        highlights.forEach(item => {
            const card = document.createElement('li');
            card.className = 'metadata-card';
            card.innerHTML = `
                <strong>${item.label}</strong>
                <span>${item.value}</span>
            `;
            list.appendChild(card);
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
            <div class="college-head">
                <div>
                    <div class="college-item-name">${college.name}</div>
                    <div class="college-item-location">📍 ${college.location}</div>
                </div>
                <div class="college-item-resources">🔥 ${resourceCount} resource${resourceCount !== 1 ? 's' : ''}</div>
            </div>
        `;

        const details = document.createElement('div');
        details.className = 'college-details';
        this.populateCollegeDetails(details, college);

        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'toggle-details';
        toggleBtn.textContent = 'View details';
        toggleBtn.setAttribute('aria-expanded', 'false');
        toggleBtn.addEventListener('click', () => this.toggleDetails(details, toggleBtn));

        listItem.appendChild(details);
        listItem.appendChild(toggleBtn);

        listItem.addEventListener('click', (e) => {
            if (e.target === toggleBtn) return;
            this.zoomToCollege(college);
            this.highlightCollege(college.id);
        });

        collegeList.appendChild(listItem);
    }

    populateCollegeDetails(container, college) {
        container.innerHTML = '';
        container.appendChild(this.createMapSnapshot(college));
        const summary = document.createElement('div');
        summary.className = 'detail-summary';
        summary.textContent = `Located in ${college.location || 'the Midwest'}, ${college.resources ? college.resources.length : 0} highlighted resource${(college.resources && college.resources.length === 1) ? '' : 's'}.`;
        container.appendChild(summary);

        if (!college.resources || college.resources.length === 0) {
            const empty = document.createElement('p');
            empty.textContent = 'No resources recorded yet.';
            empty.className = 'detail-empty';
            container.appendChild(empty);
            return;
        }

        const list = document.createElement('div');
        list.className = 'detail-resource-list';
        college.resources.slice(0, 3).forEach(resource => {
            list.appendChild(this.buildDetailRow(resource));
        });

        container.appendChild(list);
    }

    createMapSnapshot(college) {
        const snapshot = document.createElement('div');
        snapshot.className = 'map-snapshot';
        const filterLabel = this.formatFilterLabel(this.currentFilter);
        const snapshotRows = [
            { icon: '📍', label: 'Campus location', value: college.location || 'Midwest region' },
            { icon: '🗺️', label: 'Active filter', value: filterLabel },
            { icon: '🌀', label: 'Map status', value: this.mapStatus || 'Search ready' }
        ];

        snapshot.innerHTML = snapshotRows.map(row => `
            <div class="map-snapshot-row">
                <span class="map-snapshot-icon">${row.icon}</span>
                <div>
                    <strong>${row.value}</strong>
                    <small>${row.label}</small>
                </div>
            </div>
        `).join('');

        return snapshot;
    }

    formatFilterLabel(filter) {
        if (!filter || filter === 'all') {
            return 'All states';
        }

        return filter
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    toggleDetails(container, button) {
        const expanded = container.classList.toggle('expanded');
        button.textContent = expanded ? 'Hide details' : 'View details';
        button.dataset.expanded = expanded;
        button.setAttribute('aria-expanded', expanded);
    }

    buildDetailRow(resource) {
        const row = document.createElement('div');
        row.className = 'detail-row';
        row.innerHTML = `
            <strong>${resource.serviceName}</strong>
            <span>${resource.department || 'General service'}</span>
            <div class="detail-contact">
                ${resource.contactPhone ? `<a href="tel:${resource.contactPhone}">📞 ${resource.contactPhone}</a>` : ''}
                ${resource.contactEmail ? `<a href="mailto:${resource.contactEmail}">✉️ ${resource.contactEmail}</a>` : ''}
                ${resource.contactWebsite ? `<a href="${resource.contactWebsite}" target="_blank" rel="noopener">🌐 website</a>` : ''}
            </div>
        `;
        return row;
    }
    createPopupContent(college) {
        const container = document.createElement('div');
        container.className = 'custom-popup';

        const header = document.createElement('div');
        header.className = 'popup-header';
        header.innerHTML = `
            <h3>${college.name}</h3>
            <p class="popup-location">${college.location || 'Midwest region'}</p>
        `;
        container.appendChild(header);

        const highlight = document.createElement('div');
        highlight.className = 'popup-highlight';
        highlight.innerHTML = `<p>High school students can connect with curated campus counseling teams for both in-person and virtual support.</p>`;
        container.appendChild(highlight);

        const filterLabel = this.formatFilterLabel(this.currentFilter);
        const stats = document.createElement('div');
        stats.className = 'popup-info-grid';
        stats.innerHTML = `
            <div>
                <span>Filter</span>
                <strong>${filterLabel}</strong>
            </div>
            <div>
                <span>Resources in view</span>
                <strong>${college.resources ? college.resources.length : 0}</strong>
            </div>
            <div>
                <span>Map status</span>
                <strong>${this.mapStatus}</strong>
            </div>
            <div>
                <span>Campus site</span>
                <strong><a href="${college.website || '#'}" target="_blank" rel="noopener noreferrer">Visit</a></strong>
            </div>
        `;
        container.appendChild(stats);

        if (college.resources && college.resources.length > 0) {
            const resourceGrid = document.createElement('div');
            resourceGrid.className = 'resource-grid';

            college.resources.forEach(resource => {
                const resourceDiv = this.createResourceElement(resource);
                resourceGrid.appendChild(resourceDiv);
            });

            container.appendChild(resourceGrid);
        } else {
            const placeholder = document.createElement('div');
            placeholder.className = 'popup-section';
            placeholder.innerHTML = '<h4>No campus services yet</h4><p>The resource library is expanding—check back soon for new support pathways.</p>';
            container.appendChild(placeholder);
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

        this.updateMobileStats(totalColleges, totalResources);
    }

    updateMobileStats(totalColleges, totalResources) {
        const mobileColleges = document.getElementById('stat-colleges-mobile');
        if (mobileColleges) {
            mobileColleges.textContent = totalColleges;
        }

        const mobileResources = document.getElementById('stat-resources-mobile');
        if (mobileResources) {
            mobileResources.textContent = totalResources;
        }

        const mobileCount = document.getElementById('college-count-mobile');
        if (mobileCount) {
            mobileCount.textContent = `${totalColleges} campuses`;
        }
    }

    setMapStatus(status) {
        this.mapStatus = status;
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
