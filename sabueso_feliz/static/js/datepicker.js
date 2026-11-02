/**
 * Calendario Datepicker Institucional - El Sabueso Feliz
 * Experiencia de usuario (UX/UI) moderna, accesible y pulida.
 */

(function () {
    'use strict';

    const MESES = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];

    const DIAS_SEMANA = ['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá', 'Do'];

    let popover = null;
    let inputActual = null;
    let fechaVista = new Date(); // Mes y año actualmente mostrados
    let fechaSeleccionada = null; // Fecha actualmente elegida

    // Función auxiliar: formatear fecha a YYYY-MM-DD
    function formatearFecha(anio, mes, dia) {
        const m = String(mes + 1).padStart(2, '0');
        const d = String(dia).padStart(2, '0');
        return `${anio}-${m}-${d}`;
    }

    // Función auxiliar: parsear fecha YYYY-MM-DD o DD/MM/YYYY
    function parsearFecha(valor) {
        if (!valor || typeof valor !== 'string') return null;
        valor = valor.trim();

        // Formato ISO YYYY-MM-DD
        if (/^\d{4}-\d{2}-\d{2}$/.test(valor)) {
            const [y, m, d] = valor.split('-').map(Number);
            return new Date(y, m - 1, d);
        }

        // Formato Latino DD/MM/YYYY
        if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(valor)) {
            const [d, m, y] = valor.split('/').map(Number);
            return new Date(y, m - 1, d);
        }

        return null;
    }

    // Crear el elemento DOM del Popover
    function crearPopover() {
        if (popover) return popover;

        popover = document.createElement('div');
        popover.className = 'calendario-popover';
        popover.setAttribute('role', 'dialog');
        popover.setAttribute('aria-modal', 'true');
        document.body.appendChild(popover);

        // Prevenir que clics dentro del popover lo cierren
        popover.addEventListener('click', function (e) {
            e.stopPropagation();
        });

        return popover;
    }

    // Renderizar el contenido del calendario según fechaVista
    function renderizarCalendario() {
        if (!popover) return;

        const anio = fechaVista.getFullYear();
        const mes = fechaVista.getMonth();
        const hoy = new Date();

        // Calcular primer día del mes (0=Dom, 1=Lun, ..., 6=Sáb)
        const primerDia = new Date(anio, mes, 1).getDay();
        // Ajustar a semana comenzando en Lunes (0=Lun ... 6=Dom)
        const offsetLunes = (primerDia === 0) ? 6 : primerDia - 1;

        const totalDiasMes = new Date(anio, mes + 1, 0).getDate();
        const totalDiasMesAnterior = new Date(anio, mes, 0).getDate();

        // Generar opciones de años (desde 1940 hasta hoy + 10 años)
        const anioActual = hoy.getFullYear();
        const anioMin = 1940;
        const anioMax = anioActual + 10;
        let aniosOptions = '';
        for (let y = anioMax; y >= anioMin; y--) {
            aniosOptions += `<option value="${y}" ${y === anio ? 'selected' : ''}>${y}</option>`;
        }

        // Generar opciones de meses
        let mesesOptions = '';
        MESES.forEach((nombreMes, idx) => {
            mesesOptions += `<option value="${idx}" ${idx === mes ? 'selected' : ''}>${nombreMes}</option>`;
        });

        // Construir encabezado
        let html = `
            <div class="cal-cabecera">
                <button type="button" class="cal-btn-nav cal-nav-prev" title="Mes anterior" aria-label="Mes anterior">
                    <i class="bi bi-chevron-left"></i>
                </button>
                <div class="cal-selectores">
                    <select class="cal-select-mes" aria-label="Seleccionar mes">
                        ${mesesOptions}
                    </select>
                    <select class="cal-select-anio" aria-label="Seleccionar año">
                        ${aniosOptions}
                    </select>
                </div>
                <button type="button" class="cal-btn-nav cal-nav-next" title="Mes siguiente" aria-label="Mes siguiente">
                    <i class="bi bi-chevron-right"></i>
                </button>
            </div>

            <div class="cal-dias-semana">
                ${DIAS_SEMANA.map(d => `<span>${d}</span>`).join('')}
            </div>

            <div class="cal-grilla-dias">
        `;

        // Días del mes anterior
        for (let i = offsetLunes - 1; i >= 0; i--) {
            const diaNum = totalDiasMesAnterior - i;
            html += `<button type="button" class="cal-dia otro-mes cal-dia-ant" data-dia="${diaNum}">${diaNum}</button>`;
        }

        // Días del mes actual
        for (let dia = 1; dia <= totalDiasMes; dia++) {
            const esHoy = (
                dia === hoy.getDate() &&
                mes === hoy.getMonth() &&
                anio === hoy.getFullYear()
            );

            const esSeleccionado = fechaSeleccionada && (
                dia === fechaSeleccionada.getDate() &&
                mes === fechaSeleccionada.getMonth() &&
                anio === fechaSeleccionada.getFullYear()
            );

            let clases = 'cal-dia';
            if (esHoy) clases += ' hoy';
            if (esSeleccionado) clases += ' seleccionado';

            html += `<button type="button" class="${clases}" data-dia="${dia}">${dia}</button>`;
        }

        // Días del mes siguiente para completar la cuadrícula (múltiplo de 7)
        const totalCeldas = offsetLunes + totalDiasMes;
        const celdasRestantes = (totalCeldas % 7 === 0) ? 0 : 7 - (totalCeldas % 7);
        for (let d = 1; d <= celdasRestantes; d++) {
            html += `<button type="button" class="cal-dia otro-mes cal-dia-sig" data-dia="${d}">${d}</button>`;
        }

        html += `
            </div>

            <div class="cal-pie">
                <button type="button" class="cal-btn-accion cal-btn-limpiar">
                    <i class="bi bi-eraser me-1"></i>Limpiar
                </button>
                <button type="button" class="cal-btn-accion cal-btn-hoy">
                    <i class="bi bi-calendar2-check me-1"></i>Hoy
                </button>
            </div>
        `;

        popover.innerHTML = html;

        // Conectar eventos dentro del popover
        conectarEventosPopover();
    }

    // Asignar listeners a los controles internos del popover
    function conectarEventosPopover() {
        const btnPrev = popover.querySelector('.cal-nav-prev');
        const btnNext = popover.querySelector('.cal-nav-next');
        const selectMes = popover.querySelector('.cal-select-mes');
        const selectAnio = popover.querySelector('.cal-select-anio');
        const btnHoy = popover.querySelector('.cal-btn-hoy');
        const btnLimpiar = popover.querySelector('.cal-btn-limpiar');

        btnPrev.addEventListener('click', function () {
            fechaVista.setMonth(fechaVista.getMonth() - 1);
            renderizarCalendario();
        });

        btnNext.addEventListener('click', function () {
            fechaVista.setMonth(fechaVista.getMonth() + 1);
            renderizarCalendario();
        });

        selectMes.addEventListener('change', function () {
            fechaVista.setMonth(parseInt(this.value, 10));
            renderizarCalendario();
        });

        selectAnio.addEventListener('change', function () {
            fechaVista.setFullYear(parseInt(this.value, 10));
            renderizarCalendario();
        });

        btnHoy.addEventListener('click', function () {
            const hoy = new Date();
            seleccionarFecha(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());
        });

        btnLimpiar.addEventListener('click', function () {
            if (inputActual) {
                inputActual.value = '';
                inputActual.dispatchEvent(new Event('change', { bubbles: true }));
                inputActual.dispatchEvent(new Event('input', { bubbles: true }));
            }
            cerrarCalendario();
        });

        // Clic en los días
        popover.querySelectorAll('.cal-dia').forEach(btn => {
            btn.addEventListener('click', function () {
                const dia = parseInt(this.dataset.dia, 10);
                if (this.classList.contains('cal-dia-ant')) {
                    const mesAnt = new Date(fechaVista.getFullYear(), fechaVista.getMonth() - 1, dia);
                    seleccionarFecha(mesAnt.getFullYear(), mesAnt.getMonth(), dia);
                } else if (this.classList.contains('cal-dia-sig')) {
                    const mesSig = new Date(fechaVista.getFullYear(), fechaVista.getMonth() + 1, dia);
                    seleccionarFecha(mesSig.getFullYear(), mesSig.getMonth(), dia);
                } else {
                    seleccionarFecha(fechaVista.getFullYear(), fechaVista.getMonth(), dia);
                }
            });
        });
    }

    // Acción al elegir un día
    function seleccionarFecha(anio, mes, dia) {
        if (!inputActual) return;

        const valor = formatearFecha(anio, mes, dia);
        inputActual.value = valor;
        inputActual.dispatchEvent(new Event('change', { bubbles: true }));
        inputActual.dispatchEvent(new Event('input', { bubbles: true }));

        cerrarCalendario();
    }

    // Posicionar y abrir el Popover relativo al input actual
    function abrirCalendario(input) {
        crearPopover();

        inputActual = input;
        const fechaActual = parsearFecha(input.value);

        if (fechaActual && !isNaN(fechaActual.getTime())) {
            fechaSeleccionada = fechaActual;
            fechaVista = new Date(fechaActual.getFullYear(), fechaActual.getMonth(), 1);
        } else {
            fechaSeleccionada = null;
            fechaVista = new Date();
        }

        renderizarCalendario();

        // Calcular posición en pantalla
        const rect = input.getBoundingClientRect();
        const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;

        let top = rect.bottom + scrollY + 6;
        let left = rect.left + scrollX;

        // Evitar que se desborde horizontalmente hacia la derecha
        const popoverWidth = 310;
        if (left + popoverWidth > window.innerWidth - 16) {
            left = window.innerWidth - popoverWidth - 16;
        }
        if (left < 16) left = 16;

        popover.style.top = `${top}px`;
        popover.style.left = `${left}px`;

        popover.classList.add('abierto');
    }

    // Cerrar el Popover
    function cerrarCalendario() {
        if (popover && popover.classList.contains('abierto')) {
            popover.classList.remove('abierto');
            inputActual = null;
        }
    }

    // Inicializar todos los campos de fecha en el DOM
    function inicializarCamposFecha() {
        const inputs = document.querySelectorAll(
            'input.campo-fecha, input[type="date"], input[name*="fecha"]'
        );

        inputs.forEach(input => {
            // Evitar inicializar dos veces
            if (input.dataset.datepickerIniciado) return;
            input.dataset.datepickerIniciado = 'true';

            // Cambiar tipo a 'text' para desactivar el picker nativo feo del navegador
            input.type = 'text';
            input.setAttribute('autocomplete', 'off');
            input.classList.add('campo-fecha');
            if (!input.placeholder) {
                input.placeholder = 'Seleccionar fecha...';
            }

            // Envolver en contenedor con ícono elegante si no lo está
            let contenedor = input.parentElement;
            if (!contenedor.classList.contains('campo-fecha-contenedor')) {
                contenedor = document.createElement('div');
                contenedor.className = 'campo-fecha-contenedor';
                input.parentNode.insertBefore(contenedor, input);
                contenedor.appendChild(input);

                const icono = document.createElement('i');
                icono.className = 'bi bi-calendar3 campo-fecha-icono';
                contenedor.appendChild(icono);
            }

            // Abrir al hacer clic o focus
            input.addEventListener('click', function (e) {
                e.stopPropagation();
                abrirCalendario(this);
            });

            input.addEventListener('keydown', function (e) {
                if (e.key === 'Escape') {
                    cerrarCalendario();
                } else if (e.key === 'Enter') {
                    abrirCalendario(this);
                }
            });
        });
    }

    // Cerrar si se hace clic fuera del popover y de los inputs
    document.addEventListener('click', function (e) {
        if (!popover || !popover.classList.contains('abierto')) return;
        if (e.target.closest('.calendario-popover') || e.target.closest('.campo-fecha-contenedor')) {
            return;
        }
        cerrarCalendario();
    });

    // Cerrar con Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            cerrarCalendario();
        }
    });

    // Reposicionar al cambiar tamaño de ventana
    window.addEventListener('resize', function () {
        if (inputActual) {
            abrirCalendario(inputActual);
        }
    });

    // Ejecutar al cargar el documento
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inicializarCamposFecha);
    } else {
        inicializarCamposFecha();
    }

    // Exponer API global por si se renderizan nuevos campos dinámicamente
    window.SabuesoDatePicker = {
        init: inicializarCamposFecha,
        close: cerrarCalendario
    };
})();

