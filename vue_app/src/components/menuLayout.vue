<template>
    <div class="row root h-100 overflow-scroll">
        <section class="border col-md-2 col-sm-4 col-xs-12 p-0 rounded overflow-scroll">
            <nav class="navbar-expand-sm navbar-light bg-light">
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#categoryCollapse" aria-controls="categoryCollapse" aria-expanded="true">
                    <span class="bi bi-chevron-double-down"></span>
                </button>
            </nav>
            <div id="categoryCollapse" class="collapse">
                <div class="list-group" role="tablist">
                    <slot name="section"></slot>
                </div>
            </div>
        </section>
        <main class="col-md-10 col-sm-8 col-xs-12 border h-100 rounded container overflow-scroll">
            <slot name="main"></slot>
        </main>
    </div>
</template>

<style scoped>
@media (min-width: 576px) {
    section {
        height: 100%;
    }
    .collapse {
        display: block;
    }
}
.root::-webkit-scrollbar {
    display: none;
}
section::-webkit-scrollbar {
    display: none;
}
main::-webkit-scrollbar {
    display: none;
}
</style>

