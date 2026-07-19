/**
 * ESPI – Shared application JavaScript
 * Sidebar toggles, user menu, quick-add, search autocomplete
 */
window.ESPI = window.ESPI || {};

(() => {
    const toastMeta = {
        success: { title: 'Tudo certo', icon: 'check_circle' },
        error: { title: 'Não foi possível concluir', icon: 'error' },
        warning: { title: 'Atenção', icon: 'warning_amber' },
        info: { title: 'Informação', icon: 'info' },
    };

    window.ESPI.notify = (message, type = 'info', options = {}) => {
        if (!message) return null;
        const normalizedType = Object.hasOwn(toastMeta, type) ? type : 'info';
        const duration = Number(options.duration) > 0 ? Number(options.duration) : 3500;
        const region = document.getElementById('appToastRegion');
        if (!region) return null;

        const toast = document.createElement('article');
        toast.className = `app-toast app-toast--${normalizedType}`;
        toast.setAttribute('role', normalizedType === 'error' ? 'alert' : 'status');
        toast.style.setProperty('--toast-duration', `${duration}ms`);

        const icon = document.createElement('span');
        icon.className = 'app-toast__icon';
        icon.innerHTML = `<span class="material-icons-outlined">${toastMeta[normalizedType].icon}</span>`;

        const content = document.createElement('span');
        content.className = 'app-toast__content';
        const title = document.createElement('strong');
        title.className = 'app-toast__title';
        title.textContent = options.title || toastMeta[normalizedType].title;
        const body = document.createElement('span');
        body.className = 'app-toast__message';
        body.textContent = String(message);
        content.append(title, body);

        const close = document.createElement('button');
        close.type = 'button';
        close.className = 'app-toast__close';
        close.setAttribute('aria-label', 'Fechar notificação');
        close.innerHTML = '<span class="material-icons-outlined">close</span>';

        const progress = document.createElement('span');
        progress.className = 'app-toast__progress';
        toast.append(icon, content, close, progress);
        region.appendChild(toast);

        let removed = false;
        const dismiss = () => {
            if (removed) return;
            removed = true;
            toast.classList.add('is-leaving');
            window.setTimeout(() => toast.remove(), 210);
        };
        close.addEventListener('click', dismiss);
        window.setTimeout(dismiss, duration);
        return toast;
    };
})();

document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('[data-app-message]').forEach(message => {
        window.ESPI.notify(
            message.textContent.trim(),
            message.dataset.type || 'info'
        );
    });

    const errorSummary = document.querySelector('.form-error-summary__list');
    if (errorSummary) {
        const errors = Array.from(errorSummary.querySelectorAll('li'))
            .map(item => item.textContent.trim())
            .filter(Boolean);
        if (errors.length) {
            const extra = errors.length > 1 ? ` (+${errors.length - 1} campo(s))` : '';
            window.ESPI.notify(
                `${errors[0]}${extra}`,
                'error',
                { title: 'Revise o formulário' }
            );
        }
    }

    let invalidNotificationPending = false;
    document.addEventListener('invalid', event => {
        const control = event.target;
        if (!(control instanceof HTMLElement)) return;
        event.preventDefault();
        if (invalidNotificationPending) return;
        invalidNotificationPending = true;
        const form = control.closest('form');
        const label = control.id && form
            ? form.querySelector(`label[for="${control.id}"]`)
            : null;
        const fieldName = label?.textContent.replace('*', '').trim() || 'um campo obrigatório';
        window.ESPI.notify(
            `Preencha corretamente: ${fieldName}.`,
            'warning',
            { title: 'Campo obrigatório' }
        );
        control.focus({ preventScroll: true });
        control.scrollIntoView({ behavior: 'smooth', block: 'center' });
        window.setTimeout(() => { invalidNotificationPending = false; }, 450);
    }, true);

    /* ── Sidebar collapse toggle ── */
    const sidebar      = document.getElementById('sidebar');
    const collapseBtn  = document.getElementById('sidebarCollapseBtn');
    const mobileToggle = document.getElementById('mobileToggle');
    const isMobileViewport = () => window.matchMedia('(max-width: 768px)').matches;

    if (collapseBtn && sidebar) {
        collapseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (isMobileViewport()) {
                sidebar.classList.toggle('mobile-open');
                return;
            }

            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
        });
        // Restore state only on desktop/tablet
        if (!isMobileViewport() && localStorage.getItem('sidebar-collapsed') === 'true') {
            sidebar.classList.add('collapsed');
        }
    }

    if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('mobile-open');
        });
    }

    // Close mobile sidebar when clicking outside
    document.addEventListener('click', (e) => {
        if (
            sidebar &&
            sidebar.classList.contains('mobile-open') &&
            !sidebar.contains(e.target) &&
            !(mobileToggle && mobileToggle.contains(e.target))
        ) {
            sidebar.classList.remove('mobile-open');
        }
    });

    if (sidebar) {
        sidebar.querySelectorAll('a.nav-item, .nav-sub__item').forEach((item) => {
            item.addEventListener('click', () => {
                if (isMobileViewport()) {
                    sidebar.classList.remove('mobile-open');
                }
            });
        });
    }

    window.addEventListener('resize', () => {
        if (!sidebar) return;
        if (!isMobileViewport()) {
            sidebar.classList.remove('mobile-open');
        }
    });

    /* ── Nav sub-menu toggles ── */
    document.querySelectorAll('.nav-item--toggle').forEach(btn => {
        const targetId = btn.getAttribute('data-target');
        const submenu  = document.getElementById(targetId);
        if (!submenu) return;
        if (!btn.hasAttribute('aria-expanded')) {
            btn.setAttribute('aria-expanded', 'false');
        }

        // Auto-open if current URL matches a sub-item
        const currentPath = window.location.pathname;
        const links = submenu.querySelectorAll('a');
        let isActive = false;
        links.forEach(link => {
            if (currentPath.startsWith(link.getAttribute('href'))) {
                isActive = true;
                link.classList.add('active');
            }
        });
        if (isActive) {
            submenu.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
            btn.classList.add('active');
        }

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const open = submenu.classList.toggle('is-open');
            btn.setAttribute('aria-expanded', open);
        });
    });

    // Highlight active nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar__nav > a.nav-item').forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath === href) {
            item.classList.add('active');
        }
    });

    /* ── Quick-add menu ── */
    const quickAddBtn  = document.getElementById('quickAddBtn');
    const quickAddMenu = document.getElementById('quickAddMenu');

    if (quickAddBtn && quickAddMenu) {
        quickAddBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            quickAddMenu.classList.toggle('is-open');
        });
    }

    /* ── User dropdown ── */
    const userToggle   = document.getElementById('userMenuToggle');
    const userDropdown = document.getElementById('userMenuDropdown');

    if (userToggle && userDropdown) {
        userToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('is-open');
        });
    }

    // Close dropdowns on outside clicks
    document.addEventListener('click', (e) => {
        if (quickAddMenu && !quickAddBtn.contains(e.target)) {
            quickAddMenu.classList.remove('is-open');
        }
        if (userDropdown && !userToggle.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('is-open');
        }
    });

    /* ── Premium forms, required markers and conditional questions ── */
    const formSubtitles = {
        '/home/cadastro/adicionar': 'Registre os dados por etapas. As perguntas complementares aparecem somente quando forem necessárias.',
        '/familiares/adicionar': 'Cadastre o familiar com informações pessoais, vínculo, escolaridade, trabalho e saúde.',
        '/home/atendimentos/adicionar': 'Registre o atendimento com clareza para manter o histórico da pessoa atualizado.',
        '/atendimentos/adicionar': 'Registre o atendimento com clareza para manter o histórico da pessoa atualizado.',
        '/home/agendamentos/adicionar': 'Organize um novo compromisso informando pessoa, data, horário e finalidade.',
        '/agendamentos/adicionar': 'Organize um novo compromisso informando pessoa, data, horário e finalidade.',
    };

    const conditionalRules = [
        {
            source: 'id_uso_substancias_psicoativas',
            target: 'id_substancias_psicoativas',
            show: value => ['uso_anterior', 'uso_atual', 'uso_anterior_atual'].includes(value),
            hint: 'Informe somente quando houver uso anterior ou atual.',
        },
        {
            source: 'id_possui_comorbidade',
            target: 'id_comorbidades',
            show: value => value === 'sim',
            hint: 'Descreva o problema de saúde informado.',
        },
        {
            source: 'id_fez_ensino_superior',
            target: 'id_curso_superior',
            show: value => value === 'sim',
            hint: 'Informe o curso superior.',
        },
        {
            source: 'id_estuda_atualmente',
            target: 'id_horario_turno_estudo',
            show: value => value === 'sim',
            hint: 'Informe o horário ou turno de estudo.',
        },
        {
            source: 'id_procedencia',
            target: 'id_procedencia_outro',
            show: value => value === 'outro',
            hint: 'Especifique a outra procedência.',
        },
        {
            source: 'id_religiao',
            target: 'id_religiao_desde_quando',
            show: value => Boolean(value) && value !== 'nao_possui',
            hint: 'Informe há quanto tempo, se souber.',
        },
        {
            source: 'id_encaminhamento',
            target: 'id_encaminhamento_detalhe',
            show: value => Boolean(value),
            hint: 'Acrescente os detalhes do encaminhamento.',
        },
    ];

    const findFieldWrapper = element => element && element.closest(
        '.field, .form-field, .form-group'
    );
    const sectionHelp = {
        'Dados pessoais': 'Informações de identificação e autodeclaração da pessoa.',
        'Dados complementares': 'Dados adicionais para qualificação do cadastro.',
        'Status Ocupacional': 'Situação atual e histórico de experiência de trabalho.',
        'Saúde e uso de substâncias': 'Informações sensíveis exibidas conforme as respostas anteriores.',
        'Percurso Educacional': 'Escolaridade, série final e situação atual de estudo.',
        'Documentação': 'Documentos apresentados e itens que ainda precisam ser providenciados.',
        'Dados de documentos': 'Números de identificação e categoria da habilitação.',
        'Informações de atendimento': 'Origem e motivo da chegada ao Escritório Social.',
        'Encaminhamentos': 'Destino e detalhes dos encaminhamentos realizados.',
        'Endereço e contatos': 'Localização e meios seguros de contato.',
        'Trabalho, escolaridade e saúde': 'Perfil solicitado nos levantamentos DICAP.',
        'Documentos e contato': 'Documentação disponível e canais de contato.',
        'Contato': 'Endereço e meios de contato do familiar.',
        'Identificação': 'Dados essenciais para identificar corretamente a pessoa.',
        'Dados do atendimento': 'Características, objetivo e registro técnico do atendimento.',
        'Dados do agendamento': 'Pessoa, data, horário e finalidade do compromisso.',
        'Dados do familiar': 'Identificação, perfil DICAP, documentação, vínculo e contato.',
        'Vínculo familiar': 'Relação do familiar com a pessoa egressa ou pré-egressa.',
        'Foto e identificação': 'Atualize a imagem e os principais dados de identificação.',
        'Identificação e acesso': 'Defina os dados da conta e o perfil de acesso ao sistema.',
    };

    document.querySelectorAll('form.form, #formularioFamiliar').forEach(form => {
        form.classList.add('premium-form');
        const content = form.closest('.content');
        if (content) {
            content.classList.add('form-page');
            const title = content.querySelector(':scope > h1');
            if (title && !content.querySelector('.form-page-subtitle')) {
                const subtitle = document.createElement('p');
                subtitle.className = 'form-page-subtitle';
                subtitle.textContent = formSubtitles[window.location.pathname]
                    || (window.location.pathname.includes('/editar')
                        ? 'Revise as informações organizadas por seção e salve somente o que precisar alterar.'
                        : 'Preencha as informações abaixo. Campos adicionais serão exibidos conforme suas respostas.');
                title.insertAdjacentElement('afterend', subtitle);
            }
        }

        if (!form.querySelector('.form-required-note')) {
            const requiredNote = document.createElement('p');
            requiredNote.className = 'form-required-note';
            requiredNote.innerHTML = '<span><strong>*</strong> Campos obrigatórios</span>';
            const firstVisible = Array.from(form.children).find(
                child => child.tagName !== 'INPUT' || child.type !== 'hidden'
            );
            form.insertBefore(requiredNote, firstVisible || null);
        }

        form.querySelectorAll('.form-section > h2').forEach(heading => {
            if (heading.nextElementSibling?.classList.contains('section-description')) return;
            const description = sectionHelp[heading.textContent.trim()];
            if (!description) return;
            const paragraph = document.createElement('p');
            paragraph.className = 'section-description';
            paragraph.textContent = description;
            heading.insertAdjacentElement('afterend', paragraph);
        });

        form.querySelectorAll('[required]').forEach(control => {
            control.setAttribute('aria-required', 'true');
            if (!control.id) return;
            const label = form.querySelector(`label[for="${control.id}"]`);
            if (!label || label.querySelector('.required-marker')) return;
            const marker = document.createElement('span');
            marker.className = 'required-marker';
            marker.setAttribute('aria-hidden', 'true');
            marker.textContent = '*';
            label.appendChild(marker);
        });

        form.querySelectorAll('[data-required-label="true"]').forEach(label => {
            if (label.querySelector('.required-marker')) return;
            const marker = document.createElement('span');
            marker.className = 'required-marker';
            marker.setAttribute('aria-hidden', 'true');
            marker.textContent = '*';
            label.appendChild(marker);
        });

        conditionalRules.forEach(rule => {
            const source = form.querySelector(`#${rule.source}`);
            const target = form.querySelector(`#${rule.target}`);
            const wrapper = findFieldWrapper(target);
            if (!source || !target || !wrapper) return;

            wrapper.classList.add('is-conditional');
            if (rule.hint && !wrapper.querySelector('.conditional-hint')) {
                const hint = document.createElement('small');
                hint.className = 'conditional-hint';
                hint.textContent = rule.hint;
                wrapper.appendChild(hint);
            }

            const update = () => {
                const visible = rule.show(source.value);
                wrapper.classList.toggle('is-conditional-hidden', !visible);
                wrapper.setAttribute('aria-hidden', visible ? 'false' : 'true');
                target.disabled = !visible;
                source.setAttribute('aria-expanded', visible ? 'true' : 'false');
            };
            source.addEventListener('change', update);
            update();
        });
    });

    /* ── Search autocomplete ── */
    const searchBoxes = document.querySelectorAll('.topbar__search');
    if (!searchBoxes.length) return;

    const buildResults = (container) => {
        const results = document.createElement('div');
        results.className = 'search-results';
        results.style.display = 'none';
        container.appendChild(results);
        return results;
    };

    const fetchResults = async (query) => {
        const response = await fetch(`/agendamentos/buscar?q=${encodeURIComponent(query)}`);
        if (!response.ok) return [];
        const data = await response.json();
        return data.results || [];
    };

    searchBoxes.forEach((box, index) => {
        const input = box.querySelector('input');
        if (!input) return;
        if (!input.id) {
            input.id = index === 0 ? 'mainSearch' : `mainSearch-${index}`;
        }
        input.setAttribute('autocomplete', 'off');
        const results = buildResults(box);

        const closeResults = () => {
            results.style.display = 'none';
            results.innerHTML = '';
        };

        input.addEventListener('input', async () => {
            const query = input.value.trim();
            if (query.length < 2) { closeResults(); return; }
            const items = await fetchResults(query);
            results.innerHTML = '';
            if (!items.length) { closeResults(); return; }
            items.forEach((item) => {
                const row = document.createElement('div');
                row.className = 'search-result-item';
                row.textContent = item.text;
                row.addEventListener('click', () => {
                    window.location.href = `/cadastro/perfil/${item.id}`;
                });
                results.appendChild(row);
            });
            results.style.display = 'block';
        });

        document.addEventListener('click', (e) => {
            if (!box.contains(e.target)) closeResults();
        });
    });

});
